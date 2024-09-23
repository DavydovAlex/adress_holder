import re
from pathlib import Path

from xsdreader.xsd import Xsd
from xsdreader.sql import create_table_sql, create_comments_sql

import psycopg2 as pg

print(type(pg.connect()))
def db_create():
    pass


class TableCreator:

    def __init__(self, tablename, xml_path: Path, xsd_path: Path):
        self.name = tablename
        self.xml_path = xml_path
        self.xsd_path = xsd_path
        self.xsd = Xsd(xsd_path)

    def create_table(self,connection):
        pass


    def data_iter(self):
        if not self.xsd.is_valid(self.xml_path):
            raise Exception("Формат файла выходит за стандартный шаблон обработки")
        data_dict = self.xsd.schema.to_dict(self.data_path)
        if len(data_dict) == 1:
            print(list(data_dict.keys())[0])
            data_list = data_dict[list(data_dict.keys())[0]]
            data_list_processed = []
            for row in data_list:
                row_dict_processed = dict()
                for key, value in row.items():
                    row_dict_processed[re.sub('@', '', key)] = value
                yield row_dict_processed
        else:



if __name__ == '__main__':
    table = TableCreator('PARAMS',
                         Path(
                             r'D:\Поиск адресов\Новая папка\AS_PARAM_TYPES_20240905_750ec24d-b75f-4ff2-86d2-d9d8d1cf3530.XML'),
                         Path(r'D:\Поиск адресов\Новая папка\xsd\AS_PARAM_TYPES_2_251_20_04_01_01.xsd'))
    table.get_xsd('utf-8')
    for row in table.xml_iter():
        print(row)
    print(table.generate_create_table_sql())
    print(table.xsd.schema.is_valid(table.data_path))
