import psycopg2
from psycopg2 import sql
from contextlib import closing

from settings import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, TABLE_NAME


def create_table(cursor):
    sql_query = sql.SQL(f'''CREATE TABLE IF NOT EXISTS {TABLE_NAME}(
                        date_received DATE,
                        product_name TEXT,
                        sub_product TEXT,
                        issue TEXT,
                        sub_issue TEXT,
                        consumer_complaint_narrative TEXT,
                        company_public_response TEXT,
                        company TEXT,
                        state_name TEXT,
                        zip_code TEXT,
                        tags TEXT,
                        consumer_consent_provided TEXT,
                        submitted_via TEXT,
                        date_sent_to_company TEXT,
                        company_response_to_consumer TEXT,
                        timely_response TEXT,
                        consumer_disputed TEXT,
                        complaint_id INTEGER PRIMARY KEY
                        )''')
    cursor.execute(sql_query)


def load():
    with closing(psycopg2.connect(dbname=DB_NAME, user=DB_USER,
                                  password=DB_PASSWORD, host=DB_HOST)) as conn:
        conn.autocommit = True
        with conn.cursor() as cursor:
            create_table(cursor)

            with open('P9-ConsumerComplaints.csv', 'r') as f:
                next(f)
                cursor.copy_expert(f"""COPY {TABLE_NAME} FROM STDIN WITH (FORMAT CSV)""", f)


if __name__ == '__main__':
    load()
