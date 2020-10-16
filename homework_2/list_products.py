import psycopg2
import pandas as pd
from psycopg2 import sql
from contextlib import closing
import sys

from settings import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, TABLE_NAME


def get_products_list(cursor, start_date, end_date):
    sql_query = sql.SQL(f'''SELECT product_name, COUNT(issue) as amount_of_issues,
                            COUNT(CASE WHEN timely_response = 'Yes' THEN 1 END) as amount_of_timely_responded,
                            COUNT(CASE WHEN consumer_disputed = 'Yes' THEN 1 END) as amount_of_disputed
                            FROM {TABLE_NAME}
                            WHERE date_received >= '{start_date}'
                            AND date_received <= '{end_date}'
                            GROUP BY product_name
                            ORDER BY amount_of_issues''')
    cursor.execute(sql_query)
    return cursor.fetchall()


def main(start_date, end_date):
    with closing(psycopg2.connect(dbname=DB_NAME, user=DB_USER,
                                  password=DB_PASSWORD, host=DB_HOST)) as conn:
        conn.autocommit = True
        with conn.cursor() as cursor:
            res = get_products_list(cursor, start_date, end_date)
            df = pd.DataFrame(res, columns=['product_name', 'amount_of_issues',
                                            'amount_of_timely_responded', 'amount_of_disputed'])
            df = df.set_index('product_name')

            with pd.option_context('display.max_rows', None,
                                   'display.max_columns', None,
                                   'expand_frame_repr', None):
                print(df)


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
