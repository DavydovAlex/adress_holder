__all__ = ['DataColumn', 'DataRow', 'Xml']


from .attribute import *
from .xsd import Xsd
from datetime import datetime
from typing import Any, Iterator
import re


class DataColumn:
    __name: str
    __value: Any
    def __init__(self, name, value):
        self.__name = name
        self.__value = value

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = value


class DataRow:
    __columns: list[DataColumn]
    __xsd: Xsd
    __row: dict

    __remove_at: bool
    __to_lower: bool
    __convert_values: bool



    def __init__(self,
                 xsd_obj: Xsd,
                 row: dict,
                 remove_at=True,
                 to_lower=True,
                 convert_values=True
                ):
        self.__xsd = xsd_obj
        if remove_at:
            self.__row = row
        else:
            self.__row = row
        self.__columns = self.__get_columns()

    def get_column_by_name(self, name):
        for column in self.__columns:
            if column.name == name:
                return column
        return None

    def __transform_name(self, row: dict):
        row_processed = dict()
        for key, value in row.items():
            key_transformed = re.sub('@', '', key).lower()
            value_transformed = self.__change_value_type(value)
            row_processed[key_transformed] = value
        yield row_processed

    def __transform_value(self):
        pass

    def __get_columns(self):
        columns = []
        for attribute in self.__xsd.attributes:
            if attribute.name in self.__row:
                value = self.__change_value_type(attribute,self.__row[attribute.name])
                columns.append(DataColumn(name=attribute.name,
                                          value=value))
            else:
                columns.append(DataColumn(name=attribute.name,
                                          value=None))
        return columns

    def __change_value_type(self, attribute: Attribute, value: Any, ):
        if isinstance(attribute, AString):
            return value
        elif isinstance(attribute, ALong):
            return int(value)
        elif isinstance(attribute, AInteger):
            return int(value)
        elif isinstance(attribute, ABoolean):
            if isinstance(value, bool):
                return value
            elif isinstance(value, str):
                return True if value.lower() == 'true' else False
        elif isinstance(attribute, ADate):
            return datetime.strptime(value, '%Y-%m-%d')
        else:
            raise Exception("Не определен тип данных")

    @property
    def columns(self):
        return self.__columns

    @columns.setter
    def columns(self, value):
        raise Exception('Use "append()" to add column')


class Xml:
    __path: str
    __xsd: Xsd
    # __raw_data: dict

    def __init__(self, xsd_obj: Xsd, path):
        if not xsd_obj.schema.is_valid(path):
            raise Exception("XML файл не соотвествует схеме xsd")
        # self.__raw_data = xsd_obj.decode_xml(path)
        self.__xsd = xsd_obj
        self.__path = path

    def __get_data_list(self) -> list:
        data = self.__xsd.schema.decode(self.__path)
        if len(data) != 1:
            raise Exception("Формат файла выходит за стандартный шаблон обработки")
        data_list = data[list(data.keys())[0]]
        return data_list

    def iter_rows_dict(self) -> Iterator[dict]:
        data_list = self.__get_data_list()
        for row in data_list:
            row_processed = dict()
            for key, value in row.items():
                row_processed[re.sub('@', '', key)] = value
            yield row_processed

    def iter_rows(self) -> Iterator[DataRow]:
        for row in self.iter_rows_dict():
            yield DataRow(self.__xsd,
                          row)

    def get_rows_bunch_iter(self, bunch_size) -> Iterator[list[DataRow]]:
        bunch = []
        counter = 0
        for row in self.iter_rows():
            if counter == bunch_size:
                counter = 0
                yield bunch
                bunch = []
            counter += 1
            bunch.append(row)
        else:
            if len(bunch) != 0:
                yield bunch





