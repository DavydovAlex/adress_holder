import yaml
from dataclasses import dataclass
import os.path
import os


CONFIG_FILE = 'config.yml'

@dataclass
class ExtractedFile:
    xsd: str
    xml: str
    directory: str


class Config:
    __region: int
    __xsd_archive: str
    __xml_archive: str
    __path_to_extract: str
    __extracted_files: list[ExtractedFile]
    __data: dict

    def __init__(self, path):
        self.__data = self.__read(path)
        self.__region = self.__get_field('REGION', self.__data)
        self.__xsd_archive = self.__get_field('XSD_ARCHIVE_PATH', self.__data)
        self.__xml_archive = self.__get_field('FIAS_ARCHIVE_PATH', self.__data)
        self.__path_to_extract = self.__get_field('PATH_TO_EXTRACT', self.__data)
        files_to_extract = self.__get_field('FILES_TO_EXTRACT', self.__data)
        self.__extracted_files = []
        for file, patterns in files_to_extract.items():
            if self.__has_value(file, files_to_extract):
                xsd = self.__get_field('XSD', patterns)
                xml = self.__get_field('XML', patterns)
                self.__extracted_files.append(ExtractedFile(xsd=xsd,
                                                            xml=xml,
                                                            directory=file
                                                            )
                                              )

    def __read(self, path):
        if not os.path.exists(path):
            raise FileNotFoundError('Файл конфигурации не найден')
        with open(path, "r") as file:
            config_data = yaml.load(file, yaml.Loader)
        return config_data

    def __get_field(self, field, config: dict):
        if self.__has_value(field, config):
            return config[field]

    def __has_field(self, field, config: dict):
        if field in config:
            return True
        raise Exception('Поле "{}" отсутствует в файле конфигурации'.format(field))

    def __has_value(self, field, config: dict):
        if self.__has_field(field, config):
            if config[field] is not None:
                return True
        raise Exception('Поле "{}" не может быть пустым в файле конфигурации'.format(field))

    @property
    def region(self):
        return self.__region

    @property
    def xsd_archive(self):
        return self.__xsd_archive

    @property
    def xml_archive(self):
        return self.__xml_archive

    @property
    def extracted_files(self):
        return self.__extracted_files

    @property
    def path_to_extract(self):
        return self.__path_to_extract
