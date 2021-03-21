variable "input_bucket" {
  type = string
  description = "Input S3 bucket name"
}

variable "output_bucket" {
  type = string
  description = "Output S3 bucket name"
}

variable "lambda_libs_bucket" {
  type = string
  description = "Output S3 bucket name"
}

variable "lambda_layer_zip_name" {
  type = string
  description = "Lambda layer zip name"
}

variable "db_name" {
  type = string
  description = "Database name"
}

variable "db_username" {
  type = string
  description = "Database username"
}

variable "db_password" {
  type = string
  description = "Database password"
}