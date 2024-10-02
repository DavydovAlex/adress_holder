import abc
import re
from xml.etree.ElementTree import Element
from typing import Iterator
from xmlschema.validators.simple_types import XSD_NAMESPACE,  XSD_ATTRIBUTE

_XSD_TEMPLATE = '{{' + XSD_NAMESPACE + '}}{}'
_XSD_TEMPLATE_FIND = './/' + _XSD_TEMPLATE

_XSD_ELEMENT = _XSD_TEMPLATE.format('element')
_XSD_COMPLEX_TYPE = _XSD_TEMPLATE.format('complexType')


def is_attribute(element: Element) -> bool:
    return element.tag == XSD_ATTRIBUTE


def attributes_iter(element: Element) -> Iterator[Element]:
    attributes = element.findall('.//{}'.format(XSD_ATTRIBUTE))
    for attribute in attributes:
        yield attribute


def get(element: Element):
    types_class_list = [AInteger,
                        ALong,
                        ADate,
                        AString,
                        ABoolean]
    for cls in types_class_list:
        if cls.this_type(element):
            return cls(element)
    return AString(element)


class TYPES:
    STRING = 'string'
    INTEGER = 'integer'
    LONG = 'long'
    DATE = 'date'
    BOOLEAN = 'boolean'


class Attribute(abc.ABC):
    TYPE = None

    def __init__(self, element: Element):
        if is_attribute(element):
            self.element = element
            self.name = self._get_parameter('name')
            self.use = self._get_parameter('use')
            self.comment = self._get_comment()
            self.length = None
        else:
            raise Exception('Данный блок xsdreader файла, не может быть преобразован в Attribute')

    @property
    def db_type(self):
        if hasattr(self, '_db_type'):
            return self._db_type
        else:
            raise AttributeError("Поле '{}' класса '{}' не определено".format('db_type', type(self)))

    @db_type.setter
    def db_type(self, value):
        self._db_type = value
        


    def _get_comment(self) -> str:
        comment_element = self.element.find(_XSD_TEMPLATE_FIND.format('documentation'))
        if comment_element is not None:
            return comment_element.text
        else:
            return ''

    def _get_parameter(self, param) -> str:
        if self._has_parameter(param):
            return self.element.attrib[param]
        else:
            raise Exception('Не удается обнаружить обязательный параметр "{}"'.format(param))


    def _has_parameter(self, param) -> bool:
        if param in self.element.attrib:
            return True
        else:
            return False


    def _get_value(self, tag_name) -> str | None:
        param_search = self.element.find(_XSD_TEMPLATE_FIND.format(tag_name))
        if param_search is not None:
            return param_search.attrib['value']
        else:
            return None

    def __init_subclass__(cls):
        if Attribute.TYPE is cls.TYPE:
            raise NotImplementedError(
                "Attribute '{}' has not been overriden in class '{}'" \
                    .format('var', cls.__name__)
            )


    @classmethod
    def this_type(cls, element: Element):
        if 'type' in element.attrib:
            if re.sub('xs:','', element.attrib['type']) == cls.TYPE:
                return True
        else:
            for child in element.findall(_XSD_TEMPLATE_FIND.format('restriction')):
                if 'base' in child.attrib:
                    if re.sub('xs:', '', child.attrib['base']) == cls.TYPE:
                        return True
            return False


class AInteger(Attribute):
    TYPE = TYPES.INTEGER


class ALong(Attribute):
    TYPE = TYPES.LONG


class ADate(Attribute):
    TYPE = TYPES.DATE


class ABoolean(Attribute):
    TYPE = TYPES.BOOLEAN


class AString(Attribute):
    TYPE = TYPES.STRING

    def __init__(self, element: Element):
        super().__init__(element)
        self.length = self.__get_length()

    def __get_length(self):
        length = self._get_value('length')
        max_length = self._get_value('maxLength')
        return length or max_length



class XsdObject:
    def __init__(self, root: Element):
        self.root = root
        self.attributes = self._get_attributes()
        self.name = self._get_name()
        self.comment = self._get_comment()


    def _get_attributes(self):
        elements = attributes_iter(self.root)
        attribute_list = []
        for element in elements:
            attribute_list.append(get(element))
        return attribute_list

    def _get_name(self):
        tablename_element = self.root.find(_XSD_TEMPLATE_FIND.format('element'))
        if 'name' in tablename_element.attrib:
            tablename = tablename_element.attrib['name']
            return tablename
        else:
            raise Exception(
                'Не удается обнаружить element, имеющий аттрибут "name", необходимо проверить структуру файла')



    def _get_comment(self):
        table_comment = self.root.find(_XSD_TEMPLATE_FIND.format('documentation'))
        if hasattr(table_comment, 'text'):
            comment = table_comment.text
            return comment
        else:
            return ''