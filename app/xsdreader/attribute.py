__all__ = ['AttributeFactory', 'Attribute', 'AInteger', 'ALong', 'ADate', 'ABoolean', 'AString']

import abc
import re
from xml.etree.ElementTree import Element
from typing import Iterator
from xmlschema.validators.simple_types import XSD_NAMESPACE, XSD_ATTRIBUTE
from sqlalchemy import Table

_XSD_TEMPLATE = '{{' + XSD_NAMESPACE + '}}{}'
_XSD_TEMPLATE_FIND = './/' + _XSD_TEMPLATE

_XSD_ELEMENT = _XSD_TEMPLATE.format('element')
_XSD_COMPLEX_TYPE = _XSD_TEMPLATE.format('complexType')


class TYPES:
    STRING = 'string'
    INTEGER = 'integer'
    LONG = 'long'
    DATE = 'date'
    BOOLEAN = 'boolean'


class AttributeFactory:
    @staticmethod
    def get(element: Element):
        if not AttributeFactory.is_attribute(element):
            raise Exception('Блок xsd файла не может быть преобразован в Attribute')
        attribute_subclasses = Attribute.__subclasses__()
        for cls in attribute_subclasses:
            if AttributeFactory.__get_element_type(element) == cls.TYPE:
                return cls(element)
        else:
            default_subclass = AttributeFactory.__get_default_class()
        return default_subclass(element)

    @staticmethod
    def __get_default_class():
        attribute_subclasses = Attribute.__subclasses__()
        default_subclasses = []
        for cls in attribute_subclasses:
            if cls.IS_DEFAULT:
                default_subclasses.append(cls)
        if len(default_subclasses) == 1:
            return default_subclasses[0]
        elif len(default_subclasses) == 0:
            raise Exception('Необходимо установить "IS_DEFAULT = True" для одного из подклассов класса "Attribute"')
        elif len(default_subclasses) > 1:
            raise Exception('"IS_DEFAULT = True" должен иметь только один подкласс класса "Attribute".'
                            'Следующие классы имеют "IS_DEFAULT = True" [{}]'.
                            format(','.join((str(x) for x in default_subclasses)))
                            )

    @staticmethod
    def __get_element_type(element: Element):
        if 'type' in element.attrib:
            return re.sub('xs:', '', element.attrib['type'])
        else:
            restriction = element.find(_XSD_TEMPLATE_FIND.format('restriction'))
            if restriction is not None:
                if 'base' in restriction.attrib:
                    return re.sub('xs:', '', restriction.attrib['base'])
        return None

    @staticmethod
    def is_attribute(element: Element) -> bool:
        return element.tag == XSD_ATTRIBUTE

    @staticmethod
    def get_attribute_elements(element: Element) -> Iterator[Element]:
        attributes = element.findall('.//{}'.format(XSD_ATTRIBUTE))
        for attribute in attributes:
            yield attribute


class Attribute(abc.ABC):
    TYPE = None
    IS_DEFAULT = None
    __element: Element
    __name: str
    __use: str
    __description: str
    __length: str | None

    def __init__(self, element: Element):
        self.__element = element
        self.__name = self._get_parameter('name')
        self.__use = self._get_parameter('use')
        self.__description = self._get_description()
        self.__length = None

    @property
    def name(self):
        return self.__name

    @property
    def description(self):
        return self.__description

    @property
    def length(self):
        return self.__length

    def _get_description(self) -> str:
        comment_element = self.__element.find(_XSD_TEMPLATE_FIND.format('documentation'))
        if comment_element is not None:
            return comment_element.text
        else:
            return ''

    def _get_parameter(self, param) -> str:
        if param in self.__element.attrib:
            return self.__element.attrib[param]
        else:
            raise Exception('Не удается обнаружить обязательный параметр "{}"'.format(param))

    def _get_value(self, tag_name) -> str | None:
        param_search = self.__element.find(_XSD_TEMPLATE_FIND.format(tag_name))
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


class AInteger(Attribute):
    TYPE = TYPES.INTEGER
    IS_DEFAULT = False


class ALong(Attribute):
    TYPE = TYPES.LONG
    IS_DEFAULT = False


class ADate(Attribute):
    TYPE = TYPES.DATE
    IS_DEFAULT = False


class ABoolean(Attribute):
    TYPE = TYPES.BOOLEAN
    IS_DEFAULT = False


class AString(Attribute):
    TYPE = TYPES.STRING
    IS_DEFAULT = True

    def __init__(self, element: Element):
        super().__init__(element)
        self.__length = self.__get_length()


    def __get_length(self):
        length = self._get_value('length')
        max_length = self._get_value('maxLength')
        return length or max_length

    @property
    def length(self):
        return self.__length


