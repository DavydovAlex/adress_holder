import os.path
import yaml


def _check_property_to_None( value):
    if value is None:
        raise ValueError(f'Field "{value}" cant be empty')

class Column:

    def __init__(self,
                 name: str,
                 data_type: str,
                 comment: str,
                 length: int | None,
                 primary_key: bool):
        pass

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        _check_property_to_None(value)
        self._name = value

    @property
    def data_type(self):
        return self._data_type

    @data_type.setter
    def data_type(self, value):
        _check_property_to_None(value)
        self._data_type = value

    @property
    def comment(self):
        return self._comment

    @comment.setter
    def data_type(self, value):
        _check_property_to_None(value)
        self._comment = value

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
        _check_property_to_None(value)
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
        _check_property_to_None(value)
        self._description = value

    @property
    def db_tablename(self):
        return self._db_tablename

    @db_tablename.setter
    def db_tablename(self, value):
        _check_property_to_None(value)
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


