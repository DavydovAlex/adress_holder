import dataclasses
import os.path
import yaml
from datetime import datetime
from typing import Any
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

    def __init__(self,
                 name: str,
                 type_: str,
                 comment: str,
                 db_type: str | None = None,
                 db_name: str | None = None,
                 length: int | None = None,
                 primary_key: bool = False):
        self.name = name
        self.type_ = type_
        self.db_name = db_name
        self.db_type = db_type
        self.comment = comment
        self.length = length
        self.primary_key = primary_key

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
    def primary_key(self):
        return self._primary_key

    @primary_key.setter
    def primary_key(self, value: bool | None):
        check_value_type('primary_key', [bool], value)
        if value is None:
            self._primary_key = False
        else:
            self._primary_key = value


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

    def read_data(self, archive: Archive):
        data_file = archive.get_file(self.data_file_pattern, self.data_file_folder)
        tree = ET.parse(data_file)
        root = tree.getroot()
        self._data.clear()
        for elem in root.iter():
            self._data.append(elem)
        data_file.close()


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




