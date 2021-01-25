import os
import logging
from io import StringIO
from io import BytesIO

import pandas as pd
import boto3
import psycopg2

logger = logging.getLogger()
logger.setLevel(logging.INFO)

INPUT_BUCKET_NAME = os.environ['INPUT_BUCKET_NAME']
OUTPUT_BUCKET_NAME = os.environ['OUTPUT_BUCKET_NAME']
DB_HOST = os.environ['DB_HOST']
DB_NAME = os.environ['DB_NAME']
DB_USERNAME = os.environ['DB_USERNAME']
DB_PASSWORD = os.environ['DB_PASSWORD']


def read_csv_from_s3(bucket_name, object_key):
    logger.info(f'Reading file "{object_key}" from s3 input bucket "{bucket_name}"')

    s3 = boto3.client('s3')
    response = s3.get_object(Bucket=bucket_name, Key=object_key)
    
    file_content = StringIO(response['Body'].read().decode('utf-8'))
    df = pd.read_csv(file_content)
    return df


def filter_df(df):
    logger.info(f'Filtering dataset')

    df = df[df['Year'] >= 2015]
    return df


def write_df_to_s3(df, object_key):
    filename = object_key.split("/")[-1].replace('.csv', '.parquet')
    output_file_key = f'output-data/{filename}'

    logger.info(f'Writing file "{filename}" to s3 output bucket "{OUTPUT_BUCKET_NAME}"')

    file = BytesIO()
    df.to_parquet(file)
    file.seek(0)

    s3 = boto3.client('s3')
    response = s3.put_object(Bucket=OUTPUT_BUCKET_NAME, Body=file.read(), Key=output_file_key)

    logger.info(response)


def write_df_to_db(df):
    logger.info(f'Trying to connect to RDS PostgreSQL instance')

    try:
        conn = psycopg2.connect(host=DB_HOST, user=DB_USERNAME, password=DB_PASSWORD, dbname=DB_NAME)

        logger.info("SUCCESS: Connection to RDS PostgreSQL instance succeeded")

        with conn.cursor() as cur:
            cur.execute("""create table if not exists books (
                               id int,
                               name  text,
                               author text,
                               user_rating real,
                               reviews int,
                               price real,
                               year int,
                               genre text
                            )""")

            tmp_file = StringIO()
            df.to_csv(tmp_file, header=False)
            tmp_file.seek(0)

            logger.info(f'Writing to RDS PostgreSQL instance')

            cur.copy_expert(f"""COPY books FROM STDIN WITH (FORMAT CSV)""", tmp_file)

        conn.commit()

    except psycopg2.Error:
        logger.exception("ERROR: Unexpected error: Could not connect to PostgreSQL instance.")


def lambda_handler(event, context):
    if 'Records' in event:
        logger.info('Task triggered by s3 bucket')

        for record in event['Records']:
            bucket_name = record['s3']['bucket']['name']
            object_key = record['s3']['object']['key']

            df = read_csv_from_s3(bucket_name, object_key)
            df_filtered = filter_df(df)
            write_df_to_s3(df_filtered, object_key)
            write_df_to_db(df_filtered)

        return {'status': 'ok'}

    else:
        logger.info('Task triggered by schedule')

        s3 = boto3.client('s3')

        for obj in s3.list_objects(Bucket=INPUT_BUCKET_NAME, Prefix='input-data/')['Contents']:
            object_key = obj['Key']

            if object_key == 'input-data/':
                continue

            df = read_csv_from_s3(INPUT_BUCKET_NAME, object_key)
            df_filtered = filter_df(df)
            write_df_to_s3(df_filtered, object_key)
            write_df_to_db(df_filtered)

        return {'status': 'ok'}
