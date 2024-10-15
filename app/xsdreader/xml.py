__all__ = ['DataColumn', 'DataRow', 'Xml']

from .attribute import *
from .xsd import Xsd
from datetime import datetime
from typing import Any, Iterator
from dataclasses import dataclass
import re
import psutil
import time

@dataclass
class DataColumn:
    name: str
    value: Any

    @staticmethod
    def transform_name(column_name: str):
        return re.sub('@', '', column_name)

    @staticmethod
    def transform_value(value: Any, attribute: Attribute):
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
            raise Exception("Cannot override data type")


class DataRow:
    __columns: list[DataColumn]
    __attributes: list[Attribute]
    __row: dict

    def __init__(self,
                 attributes: list[Attribute],
                 row: dict
                 ):
        self.__attributes = attributes
        self.__row = self.__transform_names(row)
        self.__columns = self.__get_columns()

    def get_column_by_name(self, name):
        for column in self.__columns:
            if column.name == name:
                return column
        return None

    def __transform_names(self, row: dict):
        row_transformed = dict()
        for key, value in row.items():
            row_transformed[DataColumn.transform_name(key)] = value
        return row_transformed

    def __get_columns(self):
        columns = []
        for attribute in self.__attributes:
            if attribute.name in self.__row:
                columns.append(DataColumn(name=DataColumn.transform_name(attribute.name),
                                          value=DataColumn.transform_value(self.__row[attribute.name], attribute)))
            else:
                columns.append(DataColumn(name=DataColumn.transform_name(attribute.name),
                                          value=None))
        return columns

    def to_dict(self, low_keys: bool = True) -> dict:
        row = dict()
        for column in self.__columns:
            if low_keys:
                row[column.name.lower()] = column.value
            else:
                row[column.name] = column.value
        return row

    @property
    def columns(self):
        return self.__columns


class Xml:
    __path: str
    __xsd: Xsd
    __data: list

    def __init__(self, xsd_obj: Xsd, path):
        if not xsd_obj.schema.is_valid(path):
            raise Exception("XML файл не соотвествует схеме xsd")
        self.__xsd = xsd_obj
        self.__path = path
        self.__data = self.__get_data()


    def __get_data(self) -> list:
        data = self.__xsd.schema.decode(self.__path)
        if len(data) != 1:
            raise Exception("Формат файла выходит за стандартный шаблон обработки")
        data_list = data[list(data.keys())[0]]
        return data_list


    def iter_rows(self) -> Iterator[DataRow]:
        for row in self.__data:
            yield DataRow(self.__xsd.attributes,
                          row)


    def iter_bunch(self, rows_count) -> Iterator[list[DataRow]]:
        bunch = []
        counter = 0
        for row in self.iter_rows():
            if counter == rows_count:
                counter = 0
                yield bunch
                bunch = []
            counter += 1
            bunch.append(row)
        else:
            if len(bunch) != 0:
                yield bunch
