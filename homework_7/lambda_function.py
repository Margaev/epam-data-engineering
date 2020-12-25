import os
import sys
import logging
from io import StringIO

import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import boto3
import psycopg2

logger = logging.getLogger()
logger.setLevel(logging.INFO)

OUTPUT_BUCKET_NAME = 'margaev-output-data'
db_host = os.environ['DB_HOST']
db_name = os.environ['DB_NAME']
db_username = os.environ['DB_USERNAME']
db_password = os.environ['DB_PASSWORD']


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

    parquet_table = pa.Table.from_pandas(df)
    pq.write_table(parquet_table, f'/tmp/{filename}')

    with open(f'/tmp/{filename}', 'rb') as f:
        s3 = boto3.client('s3')
        response = s3.put_object(Bucket=OUTPUT_BUCKET_NAME, Body=f, Key=output_file_key)

        logger.info(response)


def write_df_to_db(df, object_key):
    logger.info(f'Trying to connect to RDS PostgreSQL instance')

    try:
        conn = psycopg2.connect(host=db_host, user=db_username, password=db_password, dbname=db_name)
    except psycopg2.Error as e:
        logger.error("ERROR: Unexpected error: Could not connect to PostgreSQL instance.")
        logger.error(e)
        sys.exit()

    logger.info("SUCCESS: Connection to RDS PostgreSQL instance succeeded")

    with conn.cursor() as cur:
        cur.execute("""create table if not exists books (id int,
                                                         name  text,
                                                         author text,
                                                         user_rating real,
                                                         reviews int,
                                                         price real,
                                                         year int,
                                                         genre text)""")

        filename = object_key.split("/")[-1]
        df.to_csv(f'/tmp/{filename}', header=False)

        logger.info(f'Writing to RDS PostgreSQL instance')
        with open(f'/tmp/{filename}', 'r') as f:
            cur.copy_expert(f"""COPY books FROM STDIN WITH (FORMAT CSV)""", f)

    conn.commit()


def lambda_handler(event, context):
    for record in event['Records']:
        bucket_name = record['s3']['bucket']['name']
        object_key = record['s3']['object']['key']

        df = read_csv_from_s3(bucket_name, object_key)
        df_filtered = filter_df(df)
        write_df_to_s3(df_filtered, object_key)
        write_df_to_db(df_filtered, object_key)
        
    return {'status': 'ok'}
