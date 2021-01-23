import configparser
import psycopg2
from sql_queries import create_table_queries, drop_table_queries


def drop_tables(cur, conn):
    for query in drop_table_queries:
        cur.execute(query)
        conn.commit()


def create_tables(cur, conn):
    for query in create_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    print('Connection ready!')
    cur = conn.cursor()
    print('Cursor ready!')

    drop_tables(cur, conn)
    print('Dropped tables! (if exists)')
    create_tables(cur, conn)
    print('Tables created!')

    conn.close()


if __name__ == "__main__":
    main()