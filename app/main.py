import os

from extract.extractor import Extractor
from xsdreader.xsd import Xsd
from xsdreader.xml import Xml
from pathlib import Path
from xsdreader.sql import QueryGenerator
from pprint import pprint
from db_worker.connection import Connection
import psycopg2
import time

DB = os.environ.get('POSTGRES_DB')
USER = os.environ.get('POSTGRES_USER')
PASSWORD = os.environ.get('POSTGRES_PASSWORD')
HOST = os.environ.get('POSTGRES_HOST')


# time.sleep(30)
connection = Connection(host=HOST, database=DB, user=USER, password=PASSWORD)
print('start')
ex = Extractor()
ex.extract()
extracted_object = ex.extracted_object
print('created')
for table in extracted_object.dirs:
    xsd = Xsd(Path(extracted_object.path) / Path(table.name) / Path(table.xsd))
    xml = Xml(xsd, Path(extracted_object.path) / Path(table.name) / Path(table.xml))
    print(QueryGenerator.create_table(xsd, table.name))
    connection.execute(QueryGenerator.create_table(xsd, table.name))
    rows_bunch = []
    bunch_size = 50000
    counter = 0
    for i, row in enumerate(xml.iter_rows()):
        if counter == bunch_size:
            counter = 0
            connection.execute(QueryGenerator.insert_rows(rows_bunch, table.name))
            rows_bunch = []
        counter += 1
        rows_bunch.append(row)
    else:
        if len(rows_bunch) != 0:
            connection.execute(QueryGenerator.insert_rows(rows_bunch, table.name))



