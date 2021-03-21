resource "aws_iam_role_policy" "lambda_policy" {
  name = "lambda_policy"
  role = aws_iam_role.lambda_role.id
  policy = file("iam/lambda_policy.json")
}

resource "aws_iam_role" "lambda_role" {
  name = "lambda_role"
  assume_role_policy = file("iam/lambda_assume_policy.json")
}

data "archive_file" "lambda" {
  type        = "zip"
  source_dir = "../lambda"
  output_path = "../lambda.zip"
}

resource "aws_lambda_function" "lambda" {
  filename = "../lambda.zip"
  function_name = "lambda_function"
  role = aws_iam_role.lambda_role.arn
  handler = "lambda_function.lambda_handler"
  timeout = 180

  runtime = "python3.8"

  layers = [aws_lambda_layer_version.lambda_layer.arn]

  environment {
    variables = {
      INPUT_BUCKET_NAME = var.input_bucket
      OUTPUT_BUCKET_NAME = var.output_bucket
      DB_HOST = aws_db_instance.database.address
      DB_NAME = var.db_name
      DB_USERNAME = var.db_username
      DB_PASSWORD = var.db_password
    }
  }
}

resource "aws_lambda_layer_version" "lambda_layer" {
  layer_name = "lambda_layer"
  s3_bucket = var.lambda_libs_bucket
  s3_key = var.lambda_layer_zip_name
  compatible_runtimes = ["python3.8"]
  depends_on = [aws_s3_bucket.lambda_libs_bucket]
}

resource "aws_lambda_permission" "allow_bucket" {
  statement_id = "AllowExecutionFromS3Bucket"
  action = "lambda:InvokeFunction"
  function_name = aws_lambda_function.lambda.arn
  principal = "s3.amazonaws.com"
  source_arn = aws_s3_bucket.input_bucket.arn
}

resource "aws_s3_bucket_notification" "bucket_notification" {
  bucket = aws_s3_bucket.input_bucket.id

  lambda_function {
    lambda_function_arn = aws_lambda_function.lambda.arn
    events = [
      "s3:ObjectCreated:*"]
    filter_suffix = ".csv"
  }

  depends_on = [
    aws_lambda_permission.allow_bucket]
}

resource "aws_cloudwatch_event_rule" "daily_trigger" {
  name = "daily_trigger"
  description = "Trigger lambda every day in 18:00"
  schedule_expression = "cron(00 18 ? * MON-FRI *)"
}

resource "aws_cloudwatch_event_target" "check_foo_every_five_minutes" {
  rule = aws_cloudwatch_event_rule.daily_trigger.name
  target_id = "lambda"
  arn = aws_lambda_function.lambda.arn
}

resource "aws_lambda_permission" "allow_cloudwatch_to_call_lambda" {
  statement_id = "AllowExecutionFromCloudWatch"
  action = "lambda:InvokeFunction"
  function_name = aws_lambda_function.lambda.function_name
  principal = "events.amazonaws.com"
  source_arn = aws_cloudwatch_event_rule.daily_trigger.arn
}
