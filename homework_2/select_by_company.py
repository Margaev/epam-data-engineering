import psycopg2
import pandas as pd
from psycopg2 import sql
from contextlib import closing
import sys

from settings import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, TABLE_NAME


def get_products_list(cursor, company):
    sql_query = sql.SQL(f'''select * from {TABLE_NAME}
                        where company = '{company}' and state_name = (
                            select state_name from (
                                select state_name, count(*) amount_of_complaints from complaints c 
                                where company = '{company}' and state_name is not null
                                group by state_name 
                                order by amount_of_complaints desc limit 1
                            ) state_with_max_amount_of_issues
                        );''')
    cursor.execute(sql_query)
    return cursor.fetchall()


def main(company):
    with closing(psycopg2.connect(dbname=DB_NAME, user=DB_USER,
                                  password=DB_PASSWORD, host=DB_HOST)) as conn:
        conn.autocommit = True
        with conn.cursor() as cursor:
            res = get_products_list(cursor, company)
            columns = [
                'date_received',
                'product_name',
                'sub_product',
                'issue',
                'sub_issue',
                'consumer_complaint_narrative',
                'company_public_response',
                'company',
                'state_name',
                'zip_code',
                'tags',
                'consumer_consent_provided',
                'submitted_via',
                'date_sent_to_company',
                'company_response_to_consumer',
                'timely_response',
                'consumer_disputed',
                'complaint_id'
            ]

            df = pd.DataFrame(res, columns=columns)
            df.set_index('complaint_id')

            with pd.option_context('display.max_rows', None,
                                   'display.max_columns', None,
                                   'expand_frame_repr', None):
                with open('result.csv', 'w') as f:
                    df.to_csv(f, index=False)


if __name__ == '__main__':
    main(sys.argv[1])
