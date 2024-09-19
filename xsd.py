import abc
import xml.etree.ElementTree

import xmlschema
import os.path
from pathlib import Path
from xml.etree import ElementTree
from xml.etree.ElementTree import Element
from lxml import etree
import re
import Attribute

class XsdReader:
    def __init__(self, path: Path, encoding,):
        try:
            self.path = path
            self.encoding = encoding

            self.schema = self.get_schema()
            self.raw_string = self.to_string()
        except Exception as e:
            raise e

    def get_schema(self) -> xmlschema.XMLSchema:
        return xmlschema.XMLSchema(self.path)

    def get_element_tree(self):
        return ElementTree.parse(self.path)

    def to_string(self):
        with open(self.path, encoding=self.encoding) as f:
            return f.read()


    def exclude_xs_prefix(self, xsd_string):
        return self.exclude_prefix(xsd_string, 'xs')

    def exclude_prefix(self, xsd_string, prefix):
        return re.sub(prefix + ':', '', xsd_string)

    def get_columns(self) -> list:
        xsd_without_xs = self.exclude_xs_prefix(self.raw_string)
        root_element = ElementTree.fromstring(xsd_without_xs)
        attributes = root_element.findall('.//attribute')
        columns = []
        for attribute in attributes:
            if Attribute.is_attribute(attribute):
                attribute_class = Attribute.AttributeCreator.get(attribute)
                columns.append(attribute_class)
        return columns

    def get_table_info(self):
        xsd_without_xs = self.exclude_xs_prefix(self.raw_string)
        root_element = ElementTree.fromstring(xsd_without_xs)
        tablename = root_element.find('element').attrib['name']
        table_comment = root_element.find('./element//complexType//documentation').text
        return tablename, table_comment




if __name__ =='__main__':
    filenames = ['AS_ADDR_OBJ_2',
                 'AS_ADDR_OBJ_DIVISION',
                 'AS_ADDR_OBJ_TYPES',
                 'AS_ADM_HIERARCHY',
                 'AS_APARTMENT_TYPES',
                 'AS_APARTMENTS',
                 'AS_CARPLACES',
                 'AS_CHANGE_HISTORY',
                 'AS_HOUSE_TYPES',
                 'AS_HOUSES',
                 'AS_MUN_HIERARCHY',
                 'AS_NORMATIVE_DOCS',
                 'AS_NORMATIVE_DOCS_KINDS',
                 'AS_NORMATIVE_DOCS_TYPES',
                 'AS_OBJECT_LEVELS',
                 'AS_OPERATION_TYPES',
                 'AS_PARAM',
                 'AS_PARAM_TYPES',
                 'AS_REESTR_OBJECTS',
                 'AS_ROOM_TYPES',
                 'AS_ROOMS',
                 'AS_STEADS']
    filenames =[]
    folder = r'D:\Поиск адресов\Новая папка\xsd'
    for file in os.listdir(folder):
        filenames.append(file)
    print(filenames)
    xsd_list = []
    for filename in filenames:
        xsd = XsdReader(r'D:\Поиск адресов\Новая папка\xsd',filename,isShortFilename=True, encoding='utf-8')
        xsd_list.append(xsd)
        print(xsd.get_createtable_string())
        print(xsd.get_comment_string())

