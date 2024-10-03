import os

from extract.extractor import Extractor
from pprint import pprint

ex = Extractor()
ex.extract()
extracted_object = ex.extracted_object
for table in extracted_object.dirs:
    pass