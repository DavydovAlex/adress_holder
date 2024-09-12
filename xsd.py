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




class Attribute(abc.ABC):
    TYPE = 'attribute'
    def __init__(self, element: Element):
        self.element = element
        self.name = self.get_name()
        self.use = self.get_use()
        self.documentation = self.get_documentation()

        self.enumeration = None
        self.pattern = None
        self.totalDigits = None
        self.minLength = None
        self.maxLength = None
        self.length = None

    def get_documentation(self):
        doc_attr = self.element.find('.//documentation')
        return doc_attr.text

    def get_value(self, param):
        param_search = self.element.find('.//' + param)
        if param_search:
            return param_search.attrib['value']
        else:
            return None

    def __init_subclass__(cls):
        if Attribute.TYPE is cls.TYPE:
            raise NotImplementedError(
                "Attribute '{}' has not been overriden in class '{}'" \
                .format('var', cls.__name__)
            )

    @staticmethod
    @abc.abstractmethod
    def this_type(element: Element) -> bool:
        return element.tag == 'attribute'

    def get_name(self):
        return self.element.attrib['name']

    def get_use(self):
        return self.element.attrib['use']

    def print(self):
        print(self.__dict__)

    @classmethod
    def this_type(cls, element: Element):
        print(type(cls))
        print(cls.TYPE)
        if cls.TYPE != Attribute.TYPE:
            if 'type' in element.attrib:
                if element.attrib['type'] == cls.TYPE:
                    return True
            else:
                for child in element.findall('.//restriction'):
                    if child.attrib['base'] == cls.TYPE:
                        return True
                return False
        else:
            return element.tag == 'attribute'




class AInteger(Attribute):
    TYPE = 'integer'

    def __init__(self, element: Element):
        super().__init__(element)
        self.enumeration = self._get_enumeration()
        self.pattern = super().get_value('pattern')
        self.totalDigits = super().get_value('totalDigits')

    def _get_enumeration(self):
        enumeration = []
        for child in self.element.findall('.//enumeration'):
            enumeration.append(child.attrib['value'])
        if len(enumeration) > 0:
            return enumeration
        else:
            return None

    @staticmethod
    def this_type(element: Element) -> bool:
        if isinstance(element,Element):
            for child in element.findall('.//restriction'):
                if child.attrib['base'] == 'integer':
                    return True
            return False
        else:
            return False




class ALong(Attribute):
    TYPE = 'long'
    def __init__(self,element: Element):
        super().__init__(element)
        self.totalDigits = super().get_value('totalDigits')

    @staticmethod
    def this_type(element: Element) -> bool:
        for child in element.findall('.//restriction'):
            if child.attrib['base'] == 'long':
                return True
        return False

class ADate(Attribute):
    TYPE = 'date'
    def __init__(self, element: Element):
        super().__init__(element)
    @staticmethod
    def this_type(element: Element) -> bool:
        if 'type' in element.attrib:
            if element.attrib['type'] == 'date':
                return True
            else:
                return False
        else:
            return False

class AString(Attribute):
    TYPE = 'string'
    def __init__(self, element: Element):
        super().__init__(element)
        self.length = super().get_value('length')
        self.minLength = super().get_value('minLength')
        self.maxLength = super().get_value('maxLength')
        self.pattern = super().get_value('pattern')

    @staticmethod
    def this_type(element: Element) -> bool:
        for child in element.findall('.//restriction'):
            if child.attrib['base'] == 'string':
                return True
        return False

class ABoolean(Attribute):
    TYPE = 'boolean'
    def __init__(self, element: Element):
        super().__init__(element)
    @staticmethod
    def this_type(element: Element) -> bool:
        if 'type' in element.attrib:
            if element.attrib['type'] == 'boolean':
                return True
            else:
                return False
        else:
            return False


class AttributeGenerator:

    def __init__(self, attribute: xml.etree.ElementTree.Element):
        self.attribute = attribute
    def determine_type(self, ):
        att_types_list = [AInteger, ALong, ADate, AString, ABoolean]
        for cls in att_types_list:
            if cls.this_type(self.attribute):
                return cls(self.attribute)
        return AString(self.attribute)
    def get(attribute: xml.etree.ElementTree.Element)->Attribute:
        pass


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

