import dataclasses
import os.path
import yaml
from datetime import datetime
from typing import Any, Iterable
from dataclasses import dataclass
import functools
from abc import ABC
from copy import deepcopy
from pathlib import Path
import xml.etree.ElementTree as ET


from .archive import Archive


def _check_if_None(field: str, value):
    if value is None:
        raise ValueError(f'Field "{field}" cant be empty')

def check_value_type(field:str, allowed_types: list, value):
    for allowed_type in allowed_types:
        if isinstance(value, allowed_type):
            break
    else:
        raise TypeError(f'Field "{field}" must be {[allowed_type for allowed_type in allowed_types]}')


class Column:
    """
    Class to represent column in xml file

    Attributes
    ----------
    name : str
        Name of column in xml file
    type_ : str
        type of data(described in related xsd)
    db_name : str
        Name of column in database
    comment : str
        description of column
    db_type : str | None
        Corresponding database column type(Postgres). If None filling by corresponding value for "type_" field
    length : int | None
        length of datatype. Not None only for 'string' type
    is_empty : bool
        Shows if values in column can be empty
    primary_key : bool
        Shows if column is primary key in table

    Methods
    -------

    """

    types = [('string', 'VARCHAR'),
             ('long', 'BIGINT'),
             ('integer', 'INTEGER'),
             ('boolean', 'BOOLEAN'),
             ('date', 'DATE'),
    ]  # Correspondence between type_ and db_type

    #TODO Add date format in class init block
    date_format = '%Y-%m-%d'

    def __init__(self,
                 name: str,
                 type_: str,
                 comment: str,
                 db_type: str | None = None,
                 db_name: str | None = None,
                 length: int | None = None,
                 is_empty: bool = False,
                 primary_key: bool = False):
        self.name = name
        self.type_ = type_
        self.db_name = db_name
        self.db_type = db_type
        self.comment = comment
        self.length = length
        self.primary_key = primary_key
        self.is_empty = is_empty


    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        check_value_type('name', [str], value)
        self._name = value

    @property
    def type_(self) -> str:
        return self._type_

    @type_.setter
    def type_(self, value):
        check_value_type('type_', [str], value)
        for allowed_type, _ in Column.types:
            if allowed_type == value:
                self._type_ = value
                break
        else:
            raise ValueError(f'"{value}" is incorrect value for "type_"')

    @property
    def comment(self):
        return self._comment

    @comment.setter
    def comment(self, value):
        check_value_type('comment', [str], value)
        self._comment = value

    @property
    def db_type(self) -> str:
        return self._db_type

    @db_type.setter
    def db_type(self, value: str | None):
        check_value_type('db_type', [str, type(None)], value)
        if value is not None:
            for _, allowed_db_type in Column.types:
                if allowed_db_type == value:
                    self._db_type = value
                    break
            else:
                raise ValueError(f'"{value}" is incorrect value for "db_type"')
        else:
            for allowed_type, allowed_db_type in Column.types:
                if allowed_type == self.type_:
                    self._db_type = allowed_db_type
                    break

    @property
    def db_name(self):
        return self._db_name

    @db_name.setter
    def db_name(self, value):
        check_value_type('db_name', [str, type(None)], value)
        if value is None:
            self._db_name = self.name.lower()
        else:
            self._db_name = value

    @property
    def length(self):
        return self._length

    @length.setter
    def length(self, value: int | None):
        check_value_type('length', [int, type(None)], value)
        if self.type_ == 'string':
            self._length = value
        else:
            self._length = None

    @property
    def is_empty(self):
        return self._is_empty

    @is_empty.setter
    def is_empty(self, value: bool | None):
        check_value_type('is_empty', [bool], value)
        if value is None:
            self._is_empty = False
        else:
            self._is_empty = value
        if self._is_empty is True and self._primary_key is True:
            raise ValueError('Primary key column can not be empty')

    @property
    def primary_key(self):
        return self._primary_key

    @primary_key.setter
    def primary_key(self, value: bool | None):
        check_value_type('primary_key', [bool], value)
        if value is None:
            self._primary_key = False
        else:
            self._primary_key = value


    def convert_value(self, value: str):
        if value is None and self._is_empty is False:
            raise ValueError(f'Value "{value}" for column "{self.name}" cant be empty')
        converted_value = None
        if self.type_ == 'string':
            converted_value = value
        elif self.type_ == 'long' or self.type_ == 'integer':
            if not value.isdigit():
                raise ValueError(f'Value "{value}" for column "{self.name}" must be number')
            else:
                converted_value = int(value)
        elif self.type_ == 'boolean':
            if not value.lower() in ['true', 'false']:
                raise ValueError(f'Value "{value}" for column "{self.name}" must be boolean')
            else:
                converted_value = True if value.lower() == 'true' else False
        elif self.type_ == 'date':
            try:
                datetime.strptime(value, self.date_format)
            except ValueError:
                raise ValueError(f'Value "{value}" for column "{self.name}" does not match format "{self.date_format}"')
            converted_value = datetime.strptime(value, self.date_format)
        return converted_value

    def check_value(self, value: str):
        self.convert_value(value)





class ColumnCollection:
    """
    Class to represent set of columns in xml file

    Attributes
    ----------
    columns : tuple[Column,...]
        set of Column objects
    Methods
    -------
    """
    def __init__(self, *columns: Column):
        self._columns = []
        for column in columns:
            self._columns.append(column)

    def __getitem__(self, index):
        return self._columns[index]

    def __contains__(self, name):
        for column in self._columns:
            if column.name == name:
                return True
        else:
            return False

    def __len__(self):
        return len(self._columns)

    def __iter__(self):
        return iter(self._columns)

    def append(self, column: Column):
        for col in self._columns:
            if col.name == column.name:
                raise Exception(f'Column with this name ({col.name}) is already exists')
        else:
            if column.primary_key:
                if self.get_primary_column() is not None:
                    raise Exception('Set of columns have only one primary key')
            self._columns.append(column)

    def get_primary_column(self):
        for column in self._columns:
            if column.primary_key:
                return column
        else:
            return None

    @property
    def items(self):
        return self._columns


class Row:

    def __init__(self, columns: ColumnCollection, data: dict | ET.Element = None):
        self._columns = columns
        if data is not None:
            self._data = self._transform(data)
        else:
            self._data = []

    @property
    def columns(self):
        return self._columns

    @property
    def data(self):
        return self._data

    def _transform(self, data: dict | ET.Element):
        data_dict = dict()
        row = []
        if isinstance(data, ET.Element):
            for key, value in data.items():
                data_dict[key] = value
        elif isinstance(data, dict):
            data_dict = data
        else:
            raise TypeError('Incorrect type for raw row data')
        for column in self._columns:
            if column.name in data_dict:
                row.append(column.convert_value(data_dict[column.name]))
        return row

    def set(self, data: dict | ET.Element):
        self._data = self._transform(data)

    def get(self):
        pass








class Table:

    def __init__(self,
                 name: str,
                 data_file_pattern: str,
                 data_file_folder: str | None,
                 comment: str,
                 columns: ColumnCollection):
        self.name = name
        self.data_file_pattern = data_file_pattern
        self.data_file_folder = data_file_folder
        self.comment = comment
        self.columns = columns
        self._data = []

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        check_value_type('name', [str], value)
        self._name = value

    @property
    def data_file_pattern(self) -> str:
        return self._data_file_pattern

    @data_file_pattern.setter
    def data_file_pattern(self, value: str):
        check_value_type('data_file_pattern', [str], value)
        self._data_file_pattern = value

    @property
    def data_file_folder(self) -> str | None:
        return self._data_file_folder

    @data_file_folder.setter
    def data_file_folder(self, value: str | None):
        check_value_type('data_file_folder', [str, type(None)], value)
        self._data_file_folder = value

    @property
    def comment(self) -> str:
        return self._comment

    @comment.setter
    def comment(self, value: str):
        check_value_type('description', [str], value)
        self._comment = value

    @property
    def columns(self) -> ColumnCollection:
        return self._columns

    @columns.setter
    def columns(self, value: ColumnCollection):
        check_value_type('columns', [ColumnCollection], value)
        if len(value) == 0:
            raise ValueError('Table must have at least one column')
        if value.get_primary_column() is None:
            raise ValueError('Set of columns must have one and only one primary key')
        self._columns = value

    def read_data(self, data: Iterable):
        for row in data:
            print(Row(self._columns, row).data)


    def get_create_table_sql(self) -> str:
        sql = f'CREATE TABLE {self.name} (\n'
        for column in self.columns:
            length = f'({column.length})' if column.length is not None else ''
            primary_key = 'PRIMARY KEY' if column.primary_key else ''
            sql += f'{column.db_name} {column.db_type}{length} {primary_key},\n'
        sql = sql[0:-2] + ');\n'
        return sql


    def get_create_comments_sql(self) -> str:
        sql = f"comment on table {self.name} is '{self.comment}';\n"
        for column in self.columns:
            sql += f"comment on column {self.name}.{column.db_name} is '{column.comment}';\n"
        return sql




