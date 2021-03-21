import logging

import boto3

from aws_utils import utils

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    if 'Records' in event:
        logger.info('Task triggered by s3 bucket')

        for record in event['Records']:
            bucket_name = record['s3']['bucket']['name']
            object_key = record['s3']['object']['key']

            df = utils.read_csv_from_s3(bucket_name, object_key)
            df_filtered = utils.filter_df(df)
            utils.write_df_to_s3(df_filtered, object_key)
            utils.write_df_to_db(df_filtered)

        return {'status': 'ok'}

    else:
        logger.info('Task triggered by schedule')

        s3 = boto3.client('s3')

        for obj in s3.list_objects(Bucket=utils.INPUT_BUCKET_NAME, Prefix='input-data/')['Contents']:
            object_key = obj['Key']

            if object_key == 'input-data/':
                continue

            df = utils.read_csv_from_s3(utils.INPUT_BUCKET_NAME, object_key)
            df_filtered = utils.filter_df(df)
            utils.write_df_to_s3(df_filtered, object_key)
            utils.write_df_to_db(df_filtered)

        return {'status': 'ok'}
