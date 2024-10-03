import pprint
import re
from  xmlschema import XMLSchema
from pathlib import Path
from xml.etree import ElementTree
from xml.etree.ElementTree import Element
from app.xsdreader.attribute import Attribute, AttributeFactory
from app.xsdreader.sql import create_comments_sql, create_table_sql, insert_row_sql
from app.xsdreader.xmlreader import DataRow,DataColumn
from typing import Iterator
from xmlschema.validators.simple_types import XSD_NAMESPACE,  XSD_ATTRIBUTE

ATTRIBUTE_TEMPLATE = '{{' + XSD_NAMESPACE + '}}{}'
FIND_ATTRIBUTE_TEMPLATE = './/' + ATTRIBUTE_TEMPLATE


class Xsd:
    __schema: XMLSchema
    __root: Element
    __name: str
    __description: str
    __attributes: list[Attribute]

    def __init__(self, path: Path | str):
        self.__schema = XMLSchema(path)
        self.__root = ElementTree.parse(path).getroot()
        self.__name = self.__get_name()
        self.__description = self.__get_description()
        self.__attributes = []
        for element in AttributeFactory.get_attribute_elements(self.__root):
            self.__attributes.append(AttributeFactory.get(element))

    @property
    def name(self) -> str:
        return self.__name

    @property
    def description(self) -> str:
        return self.__description

    @property
    def attributes(self) -> list[Attribute]:
        return self.__attributes

    def is_valid_xml(self, xml_file: Path | str):
        return self.__schema.is_valid(xml_file)




    def __get_name(self):
        first_element = self.__root.find(FIND_ATTRIBUTE_TEMPLATE.format('element'))
        if 'name' in first_element.attrib:
            xsd_name = first_element.attrib['name']
            return xsd_name
        else:
            raise Exception(
                'Не удается обнаружить element, имеющий аттрибут "name", необходимо проверить структуру xsd файла')


    def __get_description(self):
        table_comment = self.__root.find(FIND_ATTRIBUTE_TEMPLATE.format('documentation'))
        if hasattr(table_comment, 'text'):
            comment = table_comment.text
            return comment
        else:
            return ''




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



if __name__ =='__main__':
    xsd = Xsd(r'D:\ext\ADDR_OBJ\AS_ADDR_OBJ_2_251_01_04_01_01.xsd')
    pprint.pprint(xsd.attributes)
    #print(create_table_sql(xsd.xsd_object))
    #print(create_comments_sql(xsd.xsd_object))
    # obj = xsd.xml_iter(r'D:\Поиск адресов\Новая папка\AS_ROOM_TYPES_20240905_63f8be2d-e2c9-4b7c-83e7-4163b3545c41.XML')
    # for row in obj:
    #     print(insert_row_sql(row, xsd.xsd_object.name))



