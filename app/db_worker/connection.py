import psycopg2
import os


class Connection:
    DB = os.environ.get('POSTGRES_DB')
    USER = os.environ.get('POSTGRES_USER')
    PASSWORD = os.environ.get('POSTGRES_PASSWORD')
    HOST = os.environ.get('HOTS')

    def __init__(self):
        self.host = Connection.HOST
        self.database = Connection.DB
        self.user = Connection.USER
        self.password = Connection.PASSWORD
        self._connection = psycopg2.connect(database=self.database, user=self.user,
                                           host=self.host, password=self.password)
        self._connection.autocommit = True
        self._cursor = self._connection.cursor()

    def execute(self, sql):
        self._cursor.execute(sql)

    def __del__(self):
        self._connection.close()
        self._cursor.close()

    @staticmethod
    def create_database():
        connection = psycopg2.connect(user=Connection.USER, host=Connection.HOST, password=Connection.PASSWORD)
        connection.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = connection.cursor()
        cursor.execute('DROP DATABASE IF EXISTS {};'.format(Connection.DB))
        cursor.execute('CREATE DATABASE {};'.format(Connection.DB))
        cursor.close()
        connection.close()

    @staticmethod
    def create_schema():
        connection = psycopg2.connect(database=Connection.DB, user=Connection.USER,
                                      host=Connection.HOST, password=Connection.PASSWORD)
        with connection:
            connection.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
            cursor = connection.cursor()
            with cursor as cur:
                cur.execute('CREATE SCHEMA IF NOT EXISTS {};'.format(Connection.USER))


