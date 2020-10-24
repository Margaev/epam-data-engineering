import psycopg2
import pandas as pd
from psycopg2 import sql
from contextlib import closing
import sys

from settings import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, TABLE_NAME


def get_products_list(cursor, title_query, genre_query=None):
    if genre_query is not None:
        sql_query = sql.SQL(f'''WITH x AS (SELECT to_tsquery('{title_query}') t_q, to_tsquery('{genre_query}') g_q)
                                SELECT movie_title, actor_1_name, genres, imdb_score
                                FROM {TABLE_NAME}, x
                                WHERE to_tsvector(movie_title) @@ t_q AND to_tsvector(genres) @@ g_q
                                ORDER BY imdb_score DESC;
                                ''')
    else:
        sql_query = sql.SQL(f'''WITH x AS (SELECT to_tsquery('{title_query}') t_q)
                                SELECT movie_title, actor_1_name, genres, imdb_score
                                FROM {TABLE_NAME}, x
                                WHERE to_tsvector(movie_title) @@ t_q
                                ORDER BY imdb_score DESC;
                                ''')

    cursor.execute(sql_query)
    return cursor.fetchall()


def main():
    if not 1 < len(sys.argv) < 4:
        print(f'usage: {sys.argv[0]} <"word1 word2 word3 ..."> [<"genre1 genre2 genre3">]')
        exit(1)

    title_query = sys.argv[1]
    title_query = title_query.strip().lower().replace(' ', '|')

    genre_query = None
    if len(sys.argv) > 2:
        genre_query = sys.argv[2]
        genre_query = genre_query.strip().lower().replace(' ', '&')

    with closing(psycopg2.connect(dbname=DB_NAME, user=DB_USER,
                                  password=DB_PASSWORD, host=DB_HOST)) as conn:
        conn.autocommit = True
        with conn.cursor() as cursor:
            res = get_products_list(cursor, title_query, genre_query)
            columns = ['movie_title', 'actor_1_name', 'genres', 'imdb_score']

            df = pd.DataFrame(res, columns=columns)

            with pd.option_context('display.max_rows', None,
                                   'display.max_columns', None,
                                   'expand_frame_repr', None):
                with open('result.csv', 'w') as f:
                    print(df)
                    df.to_csv(f, index=False)


if __name__ == '__main__':
    main()
