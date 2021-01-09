import psycopg2
import pandas as pd
from psycopg2 import sql
from contextlib import closing

from settings import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, TABLE_NAME

columns = ['movie_title', 'actor_1_name', 'genres', 'imdb_score']


def create_table(cursor):
    sql_query = sql.SQL(f'''CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
                        movie_title TEXT,
                        actor_1_name TEXT,
                        genres TEXT,
                        imdb_score REAL
                        )''')
    cursor.execute(sql_query)


def filter_file(filename):
    df = pd.read_csv('movie_metadata.csv')
    filtered_filename = filename.replace('.csv', '') + '_filtered.csv'
    df_filtered = df[columns]
    df_filtered.to_csv(filtered_filename, index=False)
    return filtered_filename


def load():
    filename = 'movie_metadata.csv'
    with closing(psycopg2.connect(dbname=DB_NAME, user=DB_USER,
                                  password=DB_PASSWORD, host=DB_HOST)) as conn:
        conn.autocommit = True
        with conn.cursor() as cursor:
            create_table(cursor)

            filtered_fn = filter_file(filename)

            with open(filtered_fn, 'r') as f:
                next(f)
                cursor.copy_expert(f"""COPY {TABLE_NAME} FROM STDIN WITH (FORMAT CSV)""", f)


if __name__ == '__main__':
    load()
