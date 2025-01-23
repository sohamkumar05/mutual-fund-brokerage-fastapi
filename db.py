import psycopg2
from psycopg2 import OperationalError, extras
import os
from dotenv import load_dotenv

load_dotenv()

CURSOR_FACTORY = extras.RealDictCursor


class Connection:
    _instance = None
    _connection = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._connection = None
        return cls._instance

    def get_connection(self):
        if self._connection is None:
            try:
                self._connection = psycopg2.connect(
                    host=os.getenv("DB_HOST"),
                    database=os.getenv("DB_NAME"),
                    user=os.getenv("DB_USER"),
                    password=os.getenv("DB_PASSWORD")
                )
            except OperationalError as e:
                print(f"Error connecting to the database: {e}")
                raise
        return self._connection

    def close_connection(self):
        if self._connection:
            self._connection.close()
            self._connection = None
