import os
from extract.extractor import Extractor
from xsdreader.xsd import Xsd
from xsdreader.xml import Xml
from pathlib import Path
from xsdreader.sql import QueryGenerator
import psycopg2
import logging
from sqlalchemy import create_engine, text, Engine, insert, select
from sqlalchemy.orm import declarative_base, registry, Session
from models import AddressObject, Base, Assotiator, AddressTypes, AddressParams,\
    AdmHierarchy, ObjectLevels, ParamTypes, Address
from sqlalchemy.sql.functions import current_date


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
        logging.info("Archives have been extracted")

        engine = create_engine("postgresql+psycopg2://{user}:{password}@{host}/{dbname}".
                               format(user=USER, password=PASSWORD, host=HOST, dbname=DB))
        create_schema(engine, USER)
        logging.info('Schema {} created'.format(USER))
        Base.metadata.create_all(engine)

        AddressObject.associate_dir(extracted_object, 'ADDR_OBJ')
        AddressTypes.associate_dir(extracted_object, 'ADDR_OBJ_TYPES')
        AddressParams.associate_dir(extracted_object, 'ADDR_OBJ_PARAMS')
        AdmHierarchy.associate_dir(extracted_object, 'ADM_HIERARCHY')
        ObjectLevels.associate_dir(extracted_object, 'OBJECT_LEVELS')
        ParamTypes.associate_dir(extracted_object, 'PARAM_TYPES')

        for model in Assotiator.get_models():
            dir_ = model.get_directory()
            #Base.metadata.create_all(engine, )
            xsd = Xsd(Path(extracted_object.path) / Path(dir_.name) / Path(dir_.xsd))
            xml = Xml(xsd, Path(extracted_object.path) / Path(dir_.name) / Path(dir_.xml))

            rows_count = 0
            with Session(bind=engine) as db:
                for rows in xml.iter_bunch(50000):
                    rows_count += len(rows)
                    model_rows = model.initialize(rows)
                    db.add_all(model_rows)
                    db.commit()
            logging.info("Table {} created".format(model.__tablename__))
            logging.info(QueryGenerator.create_table(xsd, model.__tablename__))
            logging.info("Added {} rows into {}".format(rows_count, model.__tablename__))
        with (Session(bind=engine) as db):
            kladr = db.query(AddressParams.objectid, AddressParams.value). \
                select_from(AddressParams). \
                join(ParamTypes, ParamTypes.id == AddressParams.typeid). \
                filter(ParamTypes.code == 'CODE'). \
                filter(AddressParams.enddate > current_date()).subquery()
            addresses = db.query(AddressObject.id,
                                 AddressObject.objectid,
                                 AddressObject.objectguid,
                                 AddressObject.name,
                                 AddressObject.typename,
                                 AddressObject.level
                                 ). \
                filter(AddressObject.isactive == 1). \
                filter(AddressObject.isactual == 1)
            query = db.query(AddressObject.id,
                             AddressObject.objectid,
                             AddressObject.objectguid,
                             AddressObject.name,
                             AddressObject.typename,
                             AddressObject.level,
                             kladr.c.value,
                             AdmHierarchy.path
                             ).select_from(AddressObject). \
                join(AdmHierarchy, AddressObject.objectid == AdmHierarchy.objectid). \
                join(kladr, kladr.c.objectid == AddressObject.objectid). \
                filter(AddressObject.isactive == 1). \
                filter(AddressObject.isactual == 1). \
                filter(AdmHierarchy.isactive == 1)
            for row in query.all():
                if row.level == '1':
                    continue
                path_list = row.path.split('.')
                fullpath = []
                for address in path_list:
                    address_row = addresses.filter(AddressObject.objectid == address).all()
                    if len(address_row) == 0:
                        logging.warning('Для addr_obj.id = {} не удалось ' \
                                        'составить адресную цепочку, по пути {}'.\
                                        format(row.id, row.path))
                    elif len(address_row) > 1:
                        logging.warning('Для addr_obj.id= {} элемент цепочки objectid ={} ' \
                                        'имеет больше одной актуальной записи'. \
                                        format(row.id, address))
                    else:
                        if address_row[0].level == '1':
                            continue
                        else:
                            fullpath.append('{} {}'.format(address_row[0].typename, address_row[0].name))
                addr_obj = Address(id=row.id,
                                   objectid=row.objectid,
                                   objectguid=row.objectguid,
                                   name=row.name,
                                   kladr=row.value,
                                   typename=row.typename,
                                   level=row.level,
                                   path=', '.join(fullpath))
                db.add(addr_obj)
                db.commit()

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
