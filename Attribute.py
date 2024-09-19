import abc

from xml.etree import ElementTree
from xml.etree.ElementTree import Element


def is_attribute(element: Element):
    return element.tag == 'attribute'


class DB_TYPES:
    STRING = 'VARCHAR'
    INTEGER = 'INTEGER'
    LONG = 'BIGINT'
    DATE = 'DATE'
    BOOLEAN = 'BOOLEAN'

class TYPES:
    STRING = 'string'
    INTEGER = 'integer'
    LONG = 'long'
    DATE = 'date'
    BOOLEAN = 'boolean'

    TYPES_LIST = [STRING,
                  INTEGER,
                  LONG,
                  DATE,
                  BOOLEAN]

    @classmethod
    def is_existed_type(cls, type_string):
        for type_ in cls.TYPES_LIST:
            if type_string == type_:
                return True
        return False


class AttributeCreator:

    @staticmethod
    def get(element: Element):
        types_class_list = [AInteger,
                            ALong,
                            ADate,
                            AString,
                            ABoolean]
        for cls in types_class_list:
            if cls.get_type(element) == cls.TYPE:
                return cls(element)
        return AString(element)




class Attribute(abc.ABC):
    TYPE = None
    DB_TYPE = None

    def __init__(self, element: Element):
        if is_attribute(element):
            self.element = element
            self.name = element.attrib['name']
            self.use = element.attrib['use']
            self.comment = element.find('.//documentation').text
            self.length = None
        else:
            raise Exception('Данный блок xsd файла, не может быть преобразован в Attribute')

    def _get_value(self, tag_name):
        param_search = self.element.find('.//' + tag_name)
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
        if Attribute.DB_TYPE is cls.DB_TYPE:
            raise NotImplementedError(
                "Attribute '{}' has not been overriden in class '{}'" \
                    .format('var', cls.__name__)
            )

    @classmethod
    def get_type(cls, element: Element) -> str:
        type_ = None
        if 'type' in element.attrib:
            type_ = element.attrib['type']
            if not TYPES.is_existed_type(type_):
                raise Exception('Тип {} не определен в TYPES'.format(type_))
        else:
            for child in element.findall('.//restriction'):
                type_ = child.attrib['base']
                if not TYPES.is_existed_type(type_):
                    raise Exception('Тип {} не определен в TYPES'.format(type_))
                break
        if type_ is not None:
            return type_
        else:
            return TYPES.STRING

    @classmethod
    def this_type(cls, element: Element):
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
    TYPE = TYPES.INTEGER
    DB_TYPE = DB_TYPES.INTEGER


class ALong(Attribute):
    TYPE = TYPES.LONG
    DB_TYPE = DB_TYPES.LONG


class ADate(Attribute):
    TYPE = TYPES.DATE
    DB_TYPE = DB_TYPES.DATE


class ABoolean(Attribute):
    TYPE = TYPES.BOOLEAN
    DB_TYPE = DB_TYPES.BOOLEAN


class AString(Attribute):
    TYPE = TYPES.STRING
    DB_TYPE = DB_TYPES.STRING

    def __init__(self, element: Element):
        super().__init__(element)
        self.length = self.__get_length()

    def __get_length(self):
        length = self._get_value('length')
        max_length = self._get_value('maxLength')
        return length or max_length



