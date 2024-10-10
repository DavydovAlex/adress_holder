__all__ = ['Xsd']

from xmlschema import XMLSchema
from pathlib import Path
from xml.etree import ElementTree
from xml.etree.ElementTree import Element
from .attribute import *
from xmlschema.validators.simple_types import XSD_NAMESPACE
from sqlalchemy import Table, MetaData, Column, Identity, Integer

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

    @property
    def schema(self) -> XMLSchema:
        return self.__schema


    def __get_name(self) -> str:
        first_element = self.__root.find(FIND_ATTRIBUTE_TEMPLATE.format('element'))
        if 'name' in first_element.attrib:
            xsd_name = first_element.attrib['name']
            return xsd_name
        else:
            raise Exception(
                'Не удается обнаружить element, имеющий аттрибут "name", необходимо проверить структуру xsd файла')

    def __get_description(self) -> str:
        table_comment = self.__root.find(FIND_ATTRIBUTE_TEMPLATE.format('documentation'))
        if hasattr(table_comment, 'text'):
            comment = table_comment.text
            return comment
        else:
            return ''

    def get_table(self, metadata_obj: MetaData, tablename: str = None) -> Table:
        name = self.name if tablename is None else tablename
        columns = [Column('primary_key',
                          Integer,
                          primary_key=True,
                          quote=True)]

        for attribute in self.attributes:
            columns.append(attribute.build_column())
        table = Table(name,
                      metadata_obj,
                      *columns,
                      comment=self.description,)
        return table



