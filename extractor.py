import zipfile
import yaml
import re
from dataclasses import dataclass
import os.path
import os
import shutil
CONFIG_FILE = 'extractor_config.yml'
from pathlib import Path


# with open(CONFIG_FILE, "r") as file:
#     data = yaml.load(file, yaml.Loader)
#     print(data)


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


class Extractor:
    __config: Config
    def __init__(self, config: Config):
        self.__config = config

    def extract(self):
        self.make_catalog_tree()
        self.extract_xsd()
        self.extract_xml()

    def make_catalog_tree(self):
        if not os.path.exists(self.__config.path_to_extract):
            os.mkdir(self.__config.path_to_extract)
        for extracted_file in self.__config.extracted_files:
            path_to_extract = Path(self.__config.path_to_extract) / Path(extracted_file.directory)
            if not os.path.exists(path_to_extract):
                os.mkdir(path_to_extract)

    def __find_file(self, filelist: list[tuple], mask) -> tuple:
        matches = 0
        for path, name in filelist:

            if re.fullmatch(mask, name) is not None:
                matches += 1
                filename = name
                fullpath = path
        if matches == 0:
            raise FileNotFoundError(' Не удалось найти файл по заданной маске "{}"'.
                                    format(mask))
        if matches > 1:
            raise Exception('Найдено больше одного файла по заданной маске "{}"'.
                            format(mask))
        return fullpath, filename

    def get_archive_filelist(self, archive_path, folder = None):
        with zipfile.ZipFile(archive_path, "r") as zf:
            files_list = []
            for file_path in zf.namelist():
                if folder is None:
                    if Path(file_path).parent == Path('.'):
                        files_list.append((file_path, file_path, ))
                else:
                    if Path(file_path).parent == Path(str(folder)):
                        files_list.append((file_path, str(Path(file_path).name),))
            return files_list


    def extract_xsd(self):
        try:
            if not os.path.exists(self.__config.xsd_archive):
                raise FileNotFoundError('xsd архив не найден по указанному в файле конфигурации пути')
            for extracted_file in self.__config.extracted_files:
                path_to_extract = Path(self.__config.path_to_extract) / Path(extracted_file.directory)
                archive_files = self.get_archive_filelist(self.__config.xsd_archive)
                with zipfile.ZipFile(self.__config.xsd_archive, "r") as zf:
                    zip_path, _ = self.__find_file(archive_files, extracted_file.xsd)
                    zf.extract(zip_path, path_to_extract)
        except Exception as e:
            if os.path.exists(self.__config.path_to_extract):
                shutil.rmtree(self.__config.path_to_extract)
            raise e




    def extract_xml(self):
        try:
            if not os.path.exists(self.__config.xml_archive):
                raise FileNotFoundError('xml архив не найден по указанному в файле конфигурации пути')
            for extracted_file in self.__config.extracted_files:
                path_to_extract = Path(self.__config.path_to_extract) / Path(extracted_file.directory)
                archive_files_root = self.get_archive_filelist(self.__config.xml_archive)
                archive_files_region_folder = self.get_archive_filelist(self.__config.xml_archive,
                                                                        self.__config.region)
                archive_files = archive_files_root + archive_files_region_folder
                with zipfile.ZipFile(self.__config.xml_archive, "r") as zf:
                    zip_path, zip_name = self.__find_file(archive_files, extracted_file.xml)
                    source = zf.open(zip_path)
                    target = open(os.path.join(path_to_extract, zip_name), "wb")
                    with source, target:
                        shutil.copyfileobj(source, target)
        except Exception as e:
            if os.path.exists(self.__config.path_to_extract):
                shutil.rmtree(self.__config.path_to_extract)
            raise e






if __name__ == '__main__':
    config = Config(CONFIG_FILE)
    ex = Extractor(config)
    ex.extract()
