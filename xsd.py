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
from xmlschema.validators.simple_types import XSD_NAMESPACE, XSD_ANY_TYPE, XSD_SIMPLE_TYPE, XSD_PATTERN, \
    XSD_ANY_ATOMIC_TYPE, XSD_ATTRIBUTE, XSD_ATTRIBUTE_GROUP, XSD_ANY_ATTRIBUTE, \
    XSD_MIN_INCLUSIVE, XSD_MIN_EXCLUSIVE, XSD_MAX_INCLUSIVE, XSD_MAX_EXCLUSIVE, \
    XSD_LENGTH, XSD_MIN_LENGTH, XSD_MAX_LENGTH, XSD_WHITE_SPACE, XSD_ENUMERATION, \
    XSD_LIST, XSD_ANY_SIMPLE_TYPE, XSD_UNION, XSD_RESTRICTION, XSD_ANNOTATION, \
    XSD_ASSERTION, XSD_ID, XSD_IDREF, XSD_FRACTION_DIGITS, XSD_TOTAL_DIGITS, \
    XSD_EXPLICIT_TIMEZONE, XSD_ERROR, XSD_ASSERT, XSD_QNAME



class XsdReader:
    def __init__(self, path: Path, encoding,):
        try:
            self.path = path
            self.encoding = encoding
            self.schema = self._get_schema()
        except Exception as e:
            raise e

    def _get_schema(self) -> xmlschema.XMLSchema:
        return xmlschema.XMLSchema(self.path)


    def get_columns(self) -> list:
        comp = self.schema.

        for c in comp:
            print(c)
            print(type(c))
           # print(c)
        xsd_without_xs = self.exclude_xs_prefix(self.raw_string)
        root_element = ElementTree.fromstring(xsd_without_xs)
        attributes = root_element.findall('.//attribute')

        columns = []
        for attribute in attributes:

            print(xmlschema.validators.attributes.XSD_ATTRIBUTE)
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
    xsd = XsdReader(r'D:\Поиск адресов\Новая папка\xsd\AS_MUN_HIERARCHY_2_251_10_04_01_01.xsd', encoding='utf-8')
    print(xsd.get_columns())
    print(xsd.get_comment_string())


