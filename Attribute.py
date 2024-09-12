import abc

from xml.etree import ElementTree
from xml.etree.ElementTree import Element

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

    # @classmethod
    # def this_type(cls, element: Element):
    #     print(type(cls))
    #     print(cls.TYPE)
    #     if cls.TYPE != Attribute.TYPE:
    #         if 'type' in element.attrib:
    #             if element.attrib['type'] == cls.TYPE:
    #                 return True
    #         else:
    #             for child in element.findall('.//restriction'):
    #                 if child.attrib['base'] == cls.TYPE:
    #                     return True
    #             return False
    #     else:
    #         return element.tag == 'attribute'




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
