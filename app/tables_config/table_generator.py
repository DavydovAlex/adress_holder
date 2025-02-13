import yaml
from dataclasses import dataclass
import os.path
import os
from table import Table

DATA_TYPES = ['long', 'string', 'integer', 'date', 'boolean']

class TableGenerator:
    '''
    Класс для создания объектов Table из конфигурационных yml файлов
    '''

    @staticmethod
    def get_tables(self) -> list[Table]:
        pass

    @staticmethod
    def build_table(tablename: str) -> Table:
        '''
        Создает объект Table из файла конфигурации
        Parameters
        ----------
        tablename : str
                    Имя файла конфигурации без расширения
        Returns
        -------
        Table
        '''
        config = TableGenerator._read_config_file(tablename + '.yml')

        source_file_pattern = config['source_file_pattern']
        folder = config['folder']
        description = config['description']
        columns = config['columns']
        print(config)

    @staticmethod
    def _read_config_file(path):
        if not os.path.exists(path):
            filename = os.path.basename(path)
            raise FileNotFoundError(f'File {filename} not found')
        with open(path, "r", encoding='utf-8') as table_config_file:
            return yaml.load(table_config_file, yaml.Loader)








if __name__ =='__main__':
    t = TableGenerator()
    t.build_table('ADDR_OBJ')