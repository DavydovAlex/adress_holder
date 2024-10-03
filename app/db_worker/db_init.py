from pathlib import Path
import os
from app.xsdreader.xsd import Xsd
from app.xsdreader.sql import create_comments_sql, create_table_sql, insert_row_sql
from connection import Connection
import psycopg2



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
        print("Table created {}".format(self.tablename))

    def fill_table(self, connection: Connection):
        for row in self.xsd.xml_iter(self.xml_path):
            sql = insert_row_sql(row, self.tablename)
            connection.execute(sql)
            print(sql)




