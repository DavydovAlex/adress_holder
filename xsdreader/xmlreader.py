from dataclasses import dataclass
from xsdreader.builder import XsdObject, Attribute, ABoolean, ALong, AInteger, AString, ADate
from datetime import datetime
class DataColumn:

    def __init__(self, name, value):
        self._name = name
        self._value = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value



class DataRow:

    def __init__(self, xsd_object: XsdObject =None):
        self._columns = []
        self._xsd_object =xsd_object

    @property
    def columns(self):
        if self._xsd_object is not None:
            return self._columns
        return self._columns

    @columns.setter
    def columns(self, value):
        raise Exception('Use "append()" to add column')

    def append(self, column: DataColumn):
        if self._xsd_object is not None:
            column.value = self.change_value_type(column, self._xsd_object)
        self._columns.append(column)

    def change_value_type(self, column: DataColumn, xsd_object: XsdObject):
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





