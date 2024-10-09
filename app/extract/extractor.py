import zipfile
import re
from dataclasses import dataclass
import os.path
import os
import shutil
from pathlib import Path
import pprint
from .config import Config



@dataclass
class Directory:
    xsd: str
    xml: str
    name: str

@dataclass
class ExtractedObject:
    path: str
    dirs: list[Directory]


class Extractor:
    __config: Config
    __extracted_object: ExtractedObject


    def __init__(self):
        self.__config = Config()

    def extract(self):
        self.make_catalog_tree()
        self.extract_xsd()
        self.extract_xml()
        self.__extracted_object = self.__make_extracted_object()


    def __make_extracted_object(self):
        path = self.__config.path_to_extract
        folders = []
        for name in os.listdir(path):
            if os.path.isdir(os.path.join(path, name)):
                folders.append(name)
        dirs = []
        for folder in folders:
            folder_path = os.path.join(path, folder)
            files_list = os.listdir(folder_path)
            xsd = ''
            xml = ''
            for file in files_list:
                if Path(file).suffix.lower() == '.xsd':
                    xsd = file
                elif Path(file).suffix.lower() == '.xml':
                    xml = file
            dirs.append(Directory(xsd=xsd,
                                     xml=xml,
                                     name=folder))
        return ExtractedObject(path=path,
                               dirs=dirs)

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
                    if Path(file_path).parent == Path(''):
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

    @property
    def extracted_object(self):
        return self.__extracted_object



