import abc

from xml.etree import ElementTree
from xml.etree.ElementTree import Element





class Attribute(abc.ABC):
    TYPE = 'attribute'

    class TYPES:
        STRING = 'string'
        INTEGER = 'integer'
        LONG = 'long'
        DATE = 'date'
        BOOLEAN = 'boolean'

    class DB_TYPES:
        STRING = 'VARCHAR'
        INTEGER = 'INTEGER'
        LONG = 'BIGINT'
        DATE = 'DATE'
        BOOLEAN = 'BOOLEAN'

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

    def get_name(self):
        return self.element.attrib['name']

    def get_use(self):
        return self.element.attrib['use']

    def print(self):
        print(self.__dict__)

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



    @abc.abstractmethod
    def get_params(self):
        params = dict()
        params['type'] = self.TYPE
        params['name'] = self.name
        params['use'] = self.use
        params['documentation'] = self.documentation
        return params



class AInteger(Attribute):
    TYPE = T_INTEGER

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

    def get_params(self):
        params = super().get_params()
        return params


class ALong(Attribute):
    TYPE = T_LONG
    def __init__(self,element: Element):
        super().__init__(element)
        self.totalDigits = super().get_value('totalDigits')

    def get_params(self):
        params = super().get_params()
        return params


class ADate(Attribute):
    TYPE = T_DATE
    def __init__(self, element: Element):
        super().__init__(element)

    def get_params(self):
        params = super().get_params()
        return params


class AString(Attribute):
    TYPE = T_STRING
    def __init__(self, element: Element):
        super().__init__(element)
        self.length = super().get_value('length')
        self.minLength = super().get_value('minLength')
        self.maxLength = super().get_value('maxLength')
        self.pattern = super().get_value('pattern')

    def get_params(self):
        params = super().get_params()
        if self.length or self.maxLength:
            params['length'] = self.length or self.maxLength
        return params


class ABoolean(Attribute):
    TYPE = T_BOOLEAN
    def __init__(self, element: Element):
        super().__init__(element)

    def get_params(self):
        params = super().get_params()
        return params


def determine_type(attribute: Element ):
    att_types_list = [AInteger,
                      ALong,
                      ADate,
                      AString,
                      ABoolean]
    for cls in att_types_list:
        if cls.this_type(attribute):
            return cls(attribute)
    return AString(attribute)









