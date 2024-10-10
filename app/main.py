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



def create_schema(engine: Engine, schema_name):
    with engine.connect() as connection:
        drop_schema_sql = text('DROP SCHEMA IF EXISTS {} cascade;'.format(schema_name))
        connection.execute(drop_schema_sql)
        create_schema_sql = text('CREATE SCHEMA IF NOT EXISTS {};'.format(schema_name))
        connection.execute(create_schema_sql)
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
    CREATE TABLE address_info (
    
    );
    '''


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, filename="/data/log.log", filemode="w")
    try:
        DB = os.environ.get('POSTGRES_DB')
        USER = os.environ.get('POSTGRES_USER')
        PASSWORD = os.environ.get('POSTGRES_PASSWORD')
        HOST = os.environ.get('POSTGRES_HOST')

        engine = create_engine("postgresql+psycopg2://{user}:{password}@{host}/{dbname}".
                                     format(user=USER, password=PASSWORD, host=HOST, dbname=DB))
        create_schema(engine, USER)
        # connection = engine.connect()
        Base = declarative_base()
        mapper_registry = registry()

        ex = Extractor()
        ex.extract()
        extracted_object = ex.extracted_object

        # connection = psycopg2.connect(database=DB, user=USER,
        #                               host=HOST, password=PASSWORD)
        # create_schema(connection, USER)
        models = dict()
        for directory in extracted_object.dirs:
            models[directory.name] = type(directory.name, (object,), dict())
            print(models[directory.name])
            xsd = Xsd(Path(extracted_object.path) / Path(directory.name) / Path(directory.xsd))
            xml = Xml(xsd, Path(extracted_object.path) / Path(directory.name) / Path(directory.xml))
            table_obj = xsd.get_table(Base.metadata, directory.name)
            mapper_registry.map_imperatively(models[directory.name], table_obj)
            print(Base.metadata.tables)
            # create_table(xsd, table.name, connection)
            # fill_table(xml, table.name, connection, bunch_size= 50000)



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