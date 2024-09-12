import abc
import xml.etree.ElementTree

import xmlschema
import os.path
from pathlib import Path
from xml.etree import ElementTree
from xml.etree.ElementTree import Element
from lxml import etree
import re

class XSD:
    def __init__(self, folder, filename, encoding, shortname):
        try:
            if shortname:
                counter = 0
                fullname = ''
                files = os.listdir(folder)
                for file in files:
                    if filename in file:
                        counter += 1
                        fullname = file
                if counter > 1:
                    raise Exception("Каталог содержит больше одного файла с таким именем")
                self.path = Path(folder) / fullname
            else:
                self.path = Path(folder) / filename
            self.encoding = encoding
            self.schema = self._get_schema()
            self.xml = self._get_element_tree()
            self.xml_string = self._get_xml_string()
        except Exception as e:
            raise e

    def _get_schema(self):
        return xmlschema.XMLSchema(self.path)

    def _get_element_tree(self):
        return ElementTree.parse(self.path)

    def _get_xml_string(self):
        with open(self.path, encoding=self.encoding) as f:
            return f.read()

    @staticmethod
    def exclude_xs(string):
        return XSD.exclude_prefix(string,'xs')

    @staticmethod
    def exclude_prefix(string, prefix):
        return re.sub(prefix + ':', '', string)






class TableCreator:
    def __init__(self, xsd:XSD):
        self.xsd = xsd
        self.process_xsd()






    def process_xsd(self):
        xsd_wout_xs = XSD.exclude_xs(self.xsd.xml_string)
        xml = ElementTree.fromstring(xsd_wout_xs)
        tablename = xml.find('element').attrib['name']
        print(tablename)

        attributes = xml.findall('.//attribute')
        attrs_list = []
        for attribute in attributes:
            if Attribute.this_type(attribute):
                attr = AttributeGenerator(attribute).determine_type()
                attr.print()
                print(type(attr))
                #print(type(AttributeGenerator(attribute).determine_type()))
            # print(type(arrtibute))
            # elem = {}
            # for child in arrtibute.iter():
            #     # print(child.tag, child.attrib)
            #     # if child.text:
            #     #     elem[child.tag] = child.text
            #     # if child.attrib:
            #     #     elem[child.tag] = child.attrib
            #     if child.tag == 'documentation':
            #          elem['documentation'] = child.text
            #     elif child.tag == 'attribute':
            #         for key, value in child.attrib.items():
            #             elem[key] = value
            #     elif child.tag == 'restriction':
            #         for key, value in child.attrib.items():
            #             elem[key] = value
            #     elif child.tag == 'totalDigits':
            #         elem['totalDigits'] = child.attrib['value']
            #     elif child.tag == 'minLength':
            #         elem['minLength'] = child.attrib['value']
            #     elif child.tag == 'maxLength':
            #         elem['maxLength'] = child.attrib['value']
            #     elif child.tag == 'pattern':
            #         elem['pattern'] = child.attrib['value']
            #attrs_list.append(elem)
        print(attrs_list)


    def get_tablename(self, xml_string):
        xml = ElementTree.fromstring(xml_string)
        return xml.findall('element')[0].attrib['name']

    def get_attribute_info(self, block):
        if block.tag == 'attribute':
            block_info = {}










if __name__ =='__main__':
     xsd = XSD(r'D:\Поиск адресов\Новая папка\xsd','MUN_HIERARCHY',shortname=True, encoding='utf-8')

     tc = TableCreator(xsd)

     #print(xsd.get_tablename())
     #xsd._get_schema()

