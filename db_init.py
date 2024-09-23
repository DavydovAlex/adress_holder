import re
from pathlib import Path

from xsdreader import xsd
from xsdreader.sql import create_table_sql,create_comments_sql

import psycopg2 as pg



class TableCreator:

    def __init__(self, tablename, xml_path: Path, xsd_path: Path):
        self.name = tablename
        self.__data_path = xml_path
        self.__xsd_path = xsd_path

    @property
    def schema(self):
        return self.__schema

    @schema.setter
    def schema(self, value):
        self.__schema = value

    @property
    def schema_path(self):
        return self.__xsd_path

    @schema_path.setter
    def schema_path(self, value):
        self.__schema_path = value

    @property
    def data_path(self):
        return self.__data_path

    @data_path.setter
    def data_path(self, value):
        self.__data_path = value

    def get_xsd(self, encoding):
        self.xsd = xsdreader.XsdReader(self.__xsd_path, encoding)
        return self.xsd





    def xml_iter(self):
        if self.xsd.schema.is_valid(self.data_path):
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
                raise Exception("Формат файлы выходит за стандартный шаблон обработки")


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
