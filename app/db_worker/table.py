from pathlib import Path
import os
from app.xsdreader.xsd import Xsd
from app.xsdreader.xml import Xml
from app.xsdreader.sql import QueryGenerator
from connection import Connection
from app.extract.extractor import ExtractedObject
from connection import Connection
import psycopg2


class TableCreator:
    __connection: Connection | None
    __tablename: str
    __xsd: Xsd
    __xml: Xml

    def __init__(self, xsd_obj: Xsd, xml_obj: Xml, tablename):
        self.__connection = None
        self.__tablename = tablename
        self.__xml = xml_obj
        self.__xsd = xsd_obj

    @property
    def connection(self) -> Connection:
        if self.__connection is None:
            raise Exception('Не определен объект Connection для работы с БД')
        return self.__connection

    @connection.setter
    def connection(self, value):
        self.__connection = value

    def create_table(self):
        self.connection.execute(QueryGenerator.create_table(self.__xsd, self.__tablename))

    def fill_table(self, bunch_size):
        bunch = []
        counter = 0
        for row in self.__xml.iter_rows():
            if counter == bunch_size:
                counter = 0
                self.connection.execute(QueryGenerator.insert_rows(bunch, self.__tablename))
                bunch = []
            counter += 1
            bunch.append(row)
        else:
            if len(bunch) != 0:
                self.connection.execute(QueryGenerator.insert_rows(bunch, self.__tablename))



    def rows_count(self):
        sql = 'SELECT count(1) from {}'.format(self.__tablename)
        result = self.connection.select(sql)


