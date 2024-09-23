import xmlschema
from pathlib import Path
from xml.etree import ElementTree
from xml.etree.ElementTree import Element
from xsdreader.builder import XsdObject
from xsdreader.sql import create_comments_sql, create_table_sql


class Xsd:
    def __init__(self, path: Path, encoding='utf-8'):
        try:
            self.path: Path = path
            self.encoding = encoding
            self.schema = self._get_schema()
            self.root: Element = self._get_root_element()
            self.py_class = self._get_xsd_object()
        except Exception as e:
            raise e

    def is_valid(self, xml_path: Path):
        return self.schema.is_valid(xml_path)

    def _get_schema(self) -> xmlschema.XMLSchema:
        return xmlschema.XMLSchema(self.path)

    def _get_root_element(self):
        return ElementTree.parse(self.path).getroot()

    def _get_xsd_object(self) -> XsdObject:
        xsd_obj = XsdObject(self.root)
        return xsd_obj



if __name__ =='__main__':
    xsd = Xsd(r'D:\Поиск адресов\Новая папка\xsd\AS_MUN_HIERARCHY_2_251_10_04_01_01.xsd')
    print(create_table_sql(xsd.py_class))
    print(create_comments_sql(xsd.py_class))