import re
import xmlschema
from pathlib import Path
from xml.etree import ElementTree
from xml.etree.ElementTree import Element
from app.xsdreader.builder import XsdObject
from app.xsdreader.sql import create_comments_sql, create_table_sql, insert_row_sql
from app.xsdreader.xmlreader import DataRow,DataColumn
from typing import Iterator

class Xsd:
    def __init__(self, path: Path):
        try:
            self.path: Path = path
            #self.encoding = encoding
            self.schema = self._get_schema()
            self.root: Element = self._get_root_element()
            self.xsd_object = self._get_xsd_object()
        except Exception as e:
            raise e

    def is_valid(self, xml_path: Path):
        return self.schema.is_valid(xml_path)

    def create_table_sql(self):
        table = create_table_sql(self.xsd_object)
        comment = create_comments_sql(self.xsd_object)

        return table + comment

    def _get_xml_data_list(self, xml_path: Path) -> list:
        if not self.is_valid(xml_path):
            raise Exception("XML файл не соотвествует схеме xsd")
        data = self.schema.decode(xml_path)
        if len(data) != 1:
            raise Exception("Формат файла выходит за стандартный шаблон обработки")
        data_list = data[list(data.keys())[0]]
        return data_list



    def xml_iter(self, xml_path: Path) -> Iterator[DataRow]:
        data_list = self._get_xml_data_list(xml_path)
        for row in data_list:
            row_list = []
            data_row = DataRow(self.xsd_object)
            for key, value in row.items():
                column = DataColumn(re.sub('@', '', key), value)
                data_row.append(column)
            yield data_row



    def _get_schema(self) -> xmlschema.XMLSchema:
        return xmlschema.XMLSchema(self.path)

    def _get_root_element(self):
        return ElementTree.parse(self.path).getroot()

    def _get_xsd_object(self) -> XsdObject:
        xsd_obj = XsdObject(self.root)
        return xsd_obj



if __name__ =='__main__':
    xsd = Xsd(r'D:\Поиск адресов\Новая папка\xsd\AS_ROOM_TYPES_2_251_17_04_01_01.xsd')
    #print(create_table_sql(xsd.xsd_object))
    #print(create_comments_sql(xsd.xsd_object))
    obj = xsd.xml_iter(r'D:\Поиск адресов\Новая папка\AS_ROOM_TYPES_20240905_63f8be2d-e2c9-4b7c-83e7-4163b3545c41.XML')
    for row in obj:
        print(insert_row_sql(row, xsd.xsd_object.name))

