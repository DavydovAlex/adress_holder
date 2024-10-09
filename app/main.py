import os

from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.sql import select
from extract.extractor import Extractor
from xsdreader.xsd import Xsd
from xsdreader.xml import Xml
from pathlib import Path
from xsdreader.sql import QueryGenerator
from pprint import pprint
from db_worker.connection import Connection
#from db_worker.table import TableCreator
import psycopg2
import time
from pprint import pprint

DB = os.environ.get('POSTGRES_DB')
USER = os.environ.get('POSTGRES_USER')
PASSWORD = os.environ.get('POSTGRES_PASSWORD')
HOST = os.environ.get('POSTGRES_HOST')


# engine = create_engine("postgresql+psycopg2://{user}:{password}@{host}/{dbname}".
#                          format(user=USER, password=PASSWORD, host=HOST, dbname=DB))
# engine.connect()
# metadata = MetaData()
# metadata.reflect(engine)
# pprint(metadata.tables)
# Base = automap_base(metadata=metadata)
# Base.prepare()
# print(len(Base.classes))
# addr_obj = Base.classes.addr_obj



connection = Connection(host=HOST, database=DB, user=USER, password=PASSWORD)
connection.create_schema_al()

# print('start')
# ex = Extractor()
# ex.extract()
# extracted_object = ex.extracted_object
# print('created')
# for table in extracted_object.dirs:
#     xsd = Xsd(Path(extracted_object.path) / Path(table.name) / Path(table.xsd))
#     xml = Xml(xsd, Path(extracted_object.path) / Path(table.name) / Path(table.xml))
#     table_obj = TableCreator(xsd_obj=xsd, xml_obj=xml, tablename=table.name)
#     table_obj.create_table()
#     table_obj.fill_table(50000)




