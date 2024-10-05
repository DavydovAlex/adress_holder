from app.xsdreader.attribute import  ABoolean, ALong, AInteger, AString, ADate
from xsd import Xsd
from datetime import datetime
from typing import Any


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
    __raw: dict

    def __init__(self, xsd_obj: Xsd, raw_row: dict):
        self.__columns = []
        self.__xsd = xsd_obj
        self.__raw = raw_row


    def __get(self):
        for attribute in self.__xsd.attributes:


    @property
    def columns(self):
        return self.__columns

    @columns.setter
    def columns(self, value):
        raise Exception('Use "append()" to add column')

    def append(self, column: DataColumn):
        column.value = self.__change_value_type(column, self._xsd_object)
        self._columns.append(column)

    def __change_value_type(self, column: DataColumn, xsd_object: XsdObject):
        columns_types = xsd_object.attributes
        type_ = None
        for c_t in columns_types:
            if column.name == c_t.name:
                type_ = c_t
                break
        if type_ is None:
            raise Exception("В соответствующем xsd файле отсутствует поле '{}'".format(column.name))
        if isinstance(c_t, AString):
            pass
        elif isinstance(c_t, ALong):
            return int(column.value)
        elif isinstance(c_t, AInteger):
            return int(column.value)
        elif isinstance(c_t, ABoolean):
            if isinstance(column.value, bool):
                pass
            elif isinstance(column.value, str):
                return True if column.value.lower() == 'true' else False
        elif isinstance(c_t, ADate):
            return datetime.strptime(column.value, '%Y-%m-%d')
        else:
            raise Exception("Не определен тип данных")
        return column.value


class Xml:
    __path: str
    __xsd: Xsd
    # __raw_data: dict

    def __init__(self, xsd_obj: Xsd, path):
        if not xsd_obj.is_valid_xml(path):
            raise Exception("XML файл не соотвествует схеме xsd")
        # self.__raw_data = xsd_obj.decode_xml(path)
        self.__xsd = xsd_obj
        self.__path = path

    def __get_data_list(self) -> list:
        data = self.__xsd.decode_xml(self.__path)
        if len(data) != 1:
            raise Exception("Формат файла выходит за стандартный шаблон обработки")
        data_list = data[list(data.keys())[0]]
        return data_list

    def data_iter_list(self):
        data_list = self.__get_data_list()
        for row in data_list:
            row_list = []
            data_row = DataRow(self.xsd_object)
            for key, value in row.items():
                column = DataColumn(re.sub('@', '', key), value)
                data_row.append(column)
            yield data_row




