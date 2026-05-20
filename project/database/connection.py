# connection with Postgresql
import os
import psycopg2
from psycopg2 import sql, Error, pool
from dotenv import load_dotenv

# load variables
load_dotenv(override=True)

DB_NAME = os.getenv("DB_NAME")
USER = os.getenv("DB_USER")
PASSWORD = os.getenv("DB_PASSWORD")
HOST = os.getenv("DB_HOST")
PORT = os.getenv("DB_PORT")

def create_database_if_not_exists():
    conn = psycopg2.connect(
        dbname="postgres",
        password=PASSWORD,
        host=HOST,
        port=PORT,
        user=USER,
    )
    conn.autocommit = True
    cursor = conn.cursor()
    cursor.execute(
        "SELECT 1 FROM pg_database WHERE datname = %s",
        (DB_NAME,),
    )
    exists = cursor.fetchone()

    if not exists:
        cursor.execute(sql.SQL("CREATE DATABASE {}").format(
            sql.Identifier(DB_NAME)
        ))

    cursor.close()
    conn.close()

class Connection:
    _pool = None

    @classmethod
    def initialize(cls):
        if cls._pool is None:
            try:
                cls._pool = pool.SimpleConnectionPool(
                    minconn=1,
                    maxconn=10,
                    dbname=DB_NAME,
                    user=USER,
                    password=PASSWORD,
                    host=HOST,
                    port=PORT
                )
            except Error as e:
                raise Exception(f'Error connecting to database: {e}')

        return cls._pool

    @classmethod
    def get_connection(cls):
        if cls._pool is None:
            raise Exception('Connection pool not initialized')
        return cls._pool.getconn()

    @classmethod
    def release_connections(cls, conn):
        if cls._pool:
            cls._pool.putconn(conn)