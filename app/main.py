import os

from extract.extractor import Extractor
from xsdreader.xsd import Xsd
from xsdreader.xml import Xml
from pathlib import Path
from xsdreader.sql import QueryGenerator
from pprint import pprint
from db_worker.connection import Connection

connection = Connection()
connection.create_database()
connection.create_schema()
# print('start')
# ex = Extractor()
# ex.extract()
# extracted_object = ex.extracted_object
# print('created')
# for table in extracted_object.dirs:
#     print(extracted_object.path)
#     print(Path(extracted_object.path) / Path(table.name) / Path(table.xsd))
#     print(table.xml)
#     xsd = Xsd(Path(extracted_object.path) / Path(table.name) / Path(table.xsd))
#     xml = Xml(xsd, Path(extracted_object.path) / Path(table.name) / Path(table.xml))
#     print(QueryGenerator.create_table(xsd, table.name))
#     # for row in xml.iter_rows():
#     #     print(QueryGenerator.insert_row(row,table.name))
#
# INSERT INTO ADDR_OBJ ("id","objectid","objectguid","changeid","name","typename","level","opertypeid","previd","nextid","updatedate","startdate","enddate","isactual","isactive")
# app-1       | VALUES ('1192218','959584','null','2644462','null','null','null','1','0','0','2011-09-14 00:00:00','1900-01-01 00:00:00','2079-06-06 00:00:00','1','1');

#  CREATE TABLE ADDR_OBJ (
#  "id" BIGINT(),
#  "objectid" BIGINT(),
#  "objectguid" VARCHAR(),
# "changeid" BIGINT(),
#  "name" VARCHAR(),
# "typename" VARCHAR(),
# "level" VARCHAR(),
# "opertypeid" INTEGER(),
# "previd" BIGINT(),
#  "nextid" BIGINT(),
# "updatedate" DATE(),
#  "startdate" DATE(),
#  "enddate" DATE(),
#  "isactual" INTEGER(),
# "isactive" INTEGER());