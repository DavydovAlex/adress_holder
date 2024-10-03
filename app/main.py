import os

from extract.extractor import Extractor
from pprint import pprint

ex = Extractor()
ex.extract()
pprint(ex.extracted_object)