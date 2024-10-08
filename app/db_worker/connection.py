import psycopg2
import os


class Connection:
    __host: str
    __database: str
    __user: str
    __password: str
    __connection: psycopg2.extensions.connection

    def __init__(self, host, database, user, password):
        self.__host = host
        self.__database = database
        self.__user = user
        self.__password = password
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
        create_schema_sql ='CREATE SCHEMA IF NOT EXISTS {};'.format(self.__user)
        self.execute(create_schema_sql)



