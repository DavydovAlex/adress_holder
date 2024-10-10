import os
from extract.extractor import Extractor
from xsdreader.xsd import Xsd
from xsdreader.xml import Xml
from pathlib import Path
from xsdreader.sql import QueryGenerator
import psycopg2
import logging
from sqlalchemy import create_engine, text, Engine
from sqlalchemy.orm import declarative_base, registry



def create_schema(connection: psycopg2.extensions.connection, schema: str):
    with connection.cursor() as cur:
        drop_schema_sql = 'DROP SCHEMA IF EXISTS {} cascade;'.format(schema)
        cur.execute(drop_schema_sql)
        create_schema_sql = 'CREATE SCHEMA IF NOT EXISTS {};'.format(schema)
        cur.execute(create_schema_sql)
        connection.commit()


def create_table(xsd: Xsd, tablename, connection: psycopg2.extensions.connection):
    with connection.cursor() as cursor:
        create_table_sql = QueryGenerator.create_table(xsd, tablename)
        cursor.execute(create_table_sql)
        connection.commit()
        logging.info("Table '{}' was succesfully created".format(tablename))
        logging.info(create_table_sql)

def fill_table(xml: Xml, tablename, connection: psycopg2.extensions.connection, bunch_size):
    rows_count = 0
    for rows in xml.get_rows_bunch_iter(bunch_size):
        rows_count += len(rows)
        with connection.cursor() as cursor:
            insert_rows_sql = QueryGenerator.insert_rows(rows, tablename)
            cursor.execute(insert_rows_sql)
            connection.commit()
    logging.info('В таблицу {} было добавлено {} строк'.format(tablename, rows_count))


def result_table_sql():
    sql = '''
    CREATE TABLE address_info as
    select ao.objectid,
           ao.objectguid,
           ao.name,
           ao.typename,
           ao.level,
           ah.path,
           '' fullpath
      from addr_obj ao
        JOIN adm_hierarchy ah on ao.objectid = ah.objectid
        left join (select * from addr_obj_params aop 
         join param_types pt on pt.id =aop.typeid 
                    and pt.code='CODE') p on p.objectid=ao.objectid
    where ao.isactual = 1
          and ah.isactive = 1
    '''


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, filename="/data/log.log", filemode="w")
    try:
        DB = os.environ.get('POSTGRES_DB')
        USER = os.environ.get('POSTGRES_USER')
        PASSWORD = os.environ.get('POSTGRES_PASSWORD')
        HOST = os.environ.get('POSTGRES_HOST')

        ex = Extractor()
        ex.extract()
        extracted_object = ex.extracted_object

        connection = psycopg2.connect(database=DB, user=USER,
                                      host=HOST, password=PASSWORD)
        create_schema(connection, USER)

        for directory in extracted_object.dirs:

            xsd = Xsd(Path(extracted_object.path) / Path(directory.name) / Path(directory.xsd))
            xml = Xml(xsd, Path(extracted_object.path) / Path(directory.name) / Path(directory.xml))

            create_table(xsd, directory.name, connection)
            fill_table(xml, directory.name, connection, bunch_size=50000)



    except Exception as e:
        logging.exception(str(e))
        logging.info("Исправьте ошибки и перезапустите контейнеры:\n"
                     "  Выполните последовательно команды:\n"
                     "      docker compose down\n"
                     "      docker compose up -d")
        raise

    logging.info('''
    Выполнение программы завершилось успешно:
    Для получения файла дампа выполните следующие команды:
    ''')