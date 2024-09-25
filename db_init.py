import re
from pathlib import Path
import os
from xsdreader.xsd import Xsd
from xsdreader.sql import create_comments_sql, create_table_sql, insert_row_sql
import psycopg2

def get_env_data_as_dict(path: str) -> dict:
    with open(path, 'r') as f:
        env_vars = dict()
        for line in f.readlines():
            if line.startswith('#'):
                continue
            if line.find('=') != -1:
                row = tuple(line.split('='))
                env_vars[row[0].strip()] = row[1].strip()
        return env_vars

POSTGRES_DB = os.environ.get('POSTGRES_DB') if os.environ.get('POSTGRES_DB') \
    else get_env_data_as_dict('.env')['POSTGRES_DB']
POSTGRES_USER = os.environ.get('POSTGRES_USER') if os.environ.get('POSTGRES_USER') \
    else get_env_data_as_dict('.env')['POSTGRES_USER']
POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD') if os.environ.get('POSTGRES_PASSWORD') \
    else get_env_data_as_dict('.env')['POSTGRES_PASSWORD']
HOST = 'localhost'

def db_create():
    connection = psycopg2.connect(user=POSTGRES_USER, host=HOST, password=POSTGRES_PASSWORD)
    connection.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = connection.cursor()
    cursor.execute('DROP DATABASE IF EXISTS {};'.format(POSTGRES_DB))
    cursor.execute('CREATE DATABASE {};'.format(POSTGRES_DB))
    cursor.close()
    connection.close()

def create_schema():
    connection = psycopg2.connect(database=POSTGRES_DB, user=POSTGRES_USER, host=HOST, password=POSTGRES_PASSWORD)
    with connection:
        connection.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = connection.cursor()
        with cursor as cur:
            cur.execute('CREATE SCHEMA IF NOT EXISTS {};'.format(POSTGRES_USER))

class Connection:

    def __init__(self, host, database, user, password):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self._connection = psycopg2.connect(database=database, user=user,
                                           host=host, password=password)
        self._cursor =self._connection.cursor()

    def execute(self, sql):
        self._cursor.execute(sql)

    def __del__(self):
        self._connection.close()
        self._cursor.close()





class TableCreator:
    def __init__(self, tablename, xml_path: Path, xsd_path: Path):
        self.tablename = tablename
        self.xml_path = xml_path
        self.xsd_path = xsd_path
        self.xsd = Xsd(xsd_path)

    def create_table(self, connection: Connection):
        table = create_table_sql(self.xsd.xsd_object, self.tablename)
        commnents = create_comments_sql(self.xsd.xsd_object, self.tablename)
        connection.execute(table + commnents)

    def fill_table(self, connection: Connection):
        for row in self.xsd.xml_iter(self.xml_path):
            sql = insert_row_sql(row, self.tablename)
            connection.execute(sql)



if __name__ == '__main__':
    db_create()
    create_schema()
    # table = TableCreator('PARAMS',
    #                      Path(
    #                          r'D:\Поиск адресов\Новая папка\AS_PARAM_TYPES_20240905_750ec24d-b75f-4ff2-86d2-d9d8d1cf3530.XML'),
    #                      Path(r'D:\Поиск адресов\Новая папка\xsd\AS_PARAM_TYPES_2_251_20_04_01_01.xsd'))
    # table.get_xsd('utf-8')
    # for row in table.xml_iter():
    #     print(row)
    # print(table.generate_create_table_sql())
    # print(table.xsd.schema.is_valid(table.data_path))
