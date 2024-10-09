import psycopg2
from sqlalchemy import create_engine, Engine, Connection
from sqlalchemy.sql import text
import os


class Connection:
    __host: str
    __database: str
    __user: str
    __password: str
    __connection: psycopg2.extensions.connection
    __al_connection: Connection
    __engine: Engine

    def __init__(self, host, database, user, password):
        self.__host = host
        self.__database = database
        self.__user = user
        self.__password = password
        self.__engine = create_engine("postgresql+psycopg2://{user}:{password}@{host}/{dbname}".
                                      format(user=user, password=password, host=host, dbname=database))
        self.__al_connection = self.__engine.connect()
        self.__connection = psycopg2.connect(database=database, user=user,
                                             host=host, password=password)
        # self.__create_schema()

    def execute(self, sql, commit=True):
        with self.__connection.cursor() as cursor:
            cursor.execute(sql)
            if commit:
                self.__connection.commit()

    def __del__(self):
        self.__connection.close()

    def __create_schema(self):
        drop_schema_sql = 'DROP SCHEMA IF EXISTS {} cascade;'.format(self.__user)
        self.execute(drop_schema_sql)
        create_schema_sql = 'CREATE SCHEMA IF NOT EXISTS {};'.format(self.__user)
        self.execute(create_schema_sql)

    def create_schema_al(self):

        drop_schema_sql = text('DROP SCHEMA IF EXISTS {} cascade;'.format(self.__user))
        self.__al_connection.execute(drop_schema_sql)
        create_schema_sql = text('CREATE SCHEMA IF NOT EXISTS {};'.format(self.__user))
        self.__al_connection.execute(create_schema_sql)
        self.__al_connection.commit()
