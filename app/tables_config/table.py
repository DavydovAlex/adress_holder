import dataclasses
import os.path
import yaml


def _check_if_None(value):
    if value is None:
        raise ValueError(f'Field "{value}" cant be empty')



class Column:

    @dataclasses.dataclass
    class Datatype:
        datatype: str
        db_datatype: str

    allowed_datatypes = [
        Datatype('string',
                 'VARCHAR'),
        Datatype('long',
                 'BIGINT'),
        Datatype('integer',
                 'INTEGER'),
        Datatype('boolean',
                 'BOOLEAN'),
        Datatype('date',
                 'DATE'),
    ]

    def __init__(self,
                 name: str,
                 data_type: str,
                 comment: str,
                 length: int | None = None,
                 primary_key: bool | None = None):
        self.name = name
        self.data_type = data_type
        self.db_datatype = self._get_db_datatype(data_type)
        self.comment = comment
        self.length = length
        self.primary_key = primary_key

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        _check_if_None(value)
        self._name = value

    @property
    def data_type(self):
        return self._data_type

    @data_type.setter
    def data_type(self, value):
        _check_if_None(value)
        self._check_is_valid_datatype(value)
        self._data_type = value

    @property
    def comment(self):
        return self._comment

    @comment.setter
    def comment(self, value):
        _check_if_None(value)
        self._comment = value

    @property
    def length(self):
        return self._length

    @length.setter
    def length(self, value):
        if self.data_type == 'string':
            self._length = value
        else:
            self._length = None

    @property
    def primary_key(self):
        return self._primary_key

    @primary_key.setter
    def primary_key(self, value):
        if value is None:
            self._primary_key = False
        else:
            self._primary_key = value

    @property
    def db_datatype(self):
        return self._db_datatype

    @db_datatype.setter
    def db_datatype(self, value):
        _check_if_None(value)
        self._db_datatype = value



    def _check_is_valid_datatype(self, value: str):
        valid_datatypes = set([allowed_datatype.datatype for allowed_datatype in Column.allowed_datatypes])
        if value not in valid_datatypes:
            raise ValueError(
                f'Data type "data_type" not belong to allowed types: [{', '.join(valid_datatypes)}]')

    def _get_db_datatype(self, datatype):
        self._check_is_valid_datatype(datatype)
        for allowed_datatype in Column.allowed_datatypes:
            if allowed_datatype.datatype == datatype:
                return allowed_datatype.db_datatype


class Table:

    def __init__(self, tablename: str):
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), tablename + '.yml')
        config = self._read_config_file(path)
        print(config)
        self.source_file_pattern = self._get_config_field(config, 'source_file_pattern')
        self.folder = self._get_config_field(config, 'folder')
        self.description = self._get_config_field(config, 'description')
        self.db_tablename = self._get_config_field(config, 'db_tablename')
        columns = self._get_config_field(config, 'columns')


    @property
    def source_file_pattern(self):
        return self._source_file_pattern

    @source_file_pattern.setter
    def source_file_pattern(self, value):
        _check_if_None(value)
        self._source_file_pattern = value

    @property
    def folder(self):
        return self._folder

    @folder.setter
    def folder(self, value):
        self._folder = value

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        _check_if_None(value)
        self._description = value

    @property
    def db_tablename(self):
        return self._db_tablename

    @db_tablename.setter
    def db_tablename(self, value):
        _check_if_None(value)
        self._db_tablename = value





    def _get_config_field(self, config: dict, fieldname: str):
        if fieldname in config:
            return config[fieldname]
        else:
            return None

    def _read_config_file(self, path):
        if not os.path.exists(path):
            filename = os.path.basename(path)
            raise FileNotFoundError(f'File {filename} not found')
        with open(path, "r", encoding='utf-8') as table_config_file:
            return yaml.load(table_config_file, yaml.Loader)

    @classmethod
    def create_from_config(cls,):
        pass


    # def __init__(self,
    #              name: str,
    #              source_file_pattern: str,
    #              folder: str | None,
    #              description: str,
    #              columns: list[Column]
    #              ):
    #     pass


