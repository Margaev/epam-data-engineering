import random
import datetime
import time
from contextlib import closing

import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import faker

fake = faker.Faker()

TABLE_NAME = 'customer_actions'
DB_NAME = 'postgres'
DB_USER = 'postgres'
DB_PASSWORD = 'postgres'
DB_HOST = 'postgres'


def create_table(cur):
    sql_query = sql.SQL(f'''CREATE TABLE IF NOT EXISTS {TABLE_NAME}(
                            id serial,
                            name text,
                            customer_id int,
                            type text,
                            tstamp timestamp
                        ) PARTITION BY LIST (customer_id);''')
    cur.execute(sql_query)
    for i in range(10):
        sql_query = sql.SQL(f'CREATE TABLE customer_id_{i} PARTITION OF {TABLE_NAME} FOR VALUES IN ({i});')
        cur.execute(sql_query)


def insert(cur, _name, _customer_id, _action_type, _timestamp):
    sql_query = sql.SQL(f'''
                         INSERT INTO {TABLE_NAME} (name, customer_id, type, tstamp) VALUES (
                             '{_name}', '{_customer_id}', '{_action_type}', '{_timestamp}' 
                         )
                         ''')
    cur.execute(sql_query)


with closing(psycopg2.connect(dbname=DB_NAME, user=DB_USER,
                              password=DB_PASSWORD, host=DB_HOST)) as conn:
    conn.autocommit = True

    with conn.cursor() as cursor:
        create_table(cursor)

        while True:
            name = fake.name()
            customer_id = random.choice(range(10))
            action_type = random.choice(['1', '2', '3', '4'])
            timestamp = datetime.datetime.now()
            insert(cursor, name, customer_id, action_type, timestamp)
            time.sleep(2)
