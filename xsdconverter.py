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



class XsdConverter:
    pass




class XsdObject:
    pass


class Attribute:
    pass