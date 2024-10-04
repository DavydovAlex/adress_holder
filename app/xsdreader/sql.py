from app.xsdreader.attribute import  Attribute, ABoolean, ALong, AInteger, AString, ADate
from copy import deepcopy
from xsd import Xsd
from app.xsdreader.xmlreader import DataRow


class QueryGenerator:

    @staticmethod
    def __get_db_type(attribute: Attribute) -> str:
        if isinstance(attribute, AString):
            return 'VARCHAR'
        elif isinstance(attribute, ALong):
            return 'BIGINT'
        elif isinstance(attribute, AInteger):
            return 'INTEGER'
        elif isinstance(attribute, ABoolean):
            return 'BOOLEAN'
        elif isinstance(attribute, ADate):
            return 'DATE'
        else:
            raise Exception("Не определен тип данных")

    @staticmethod
    def create_table(xsd_obj: Xsd, tablename=None) -> str:
        sql = 'CREATE TABLE {} (\n'.format(tablename if tablename is not None else xsd_obj.name)
        for attribute in xsd_obj.attributes:
            column_datatype = QueryGenerator.__get_db_type(attribute)
            sql += '"{}" {}{},\n'.format(attribute.name.lower(),
                                         column_datatype,
                                         '({})'.format(attribute.length if attribute.length is not None else ''))
        sql = sql[0:-2] + ');\n'
        return sql

    @staticmethod
    def create_comments(xsd_obj: Xsd, tablename=None):
        name = tablename if tablename is not None else xsd_obj.name
        sql = "comment on table {} is '{}';\n".format(name, xsd_obj.description)
        for attribute in xsd_obj.attributes:
            sql += "comment on column {}.{} is '{}';\n".format(name,
                                                               attribute.name.lower(),
                                                               attribute.description)
        return sql

def insert_row_sql(row:DataRow , tablename):
    columns_list = ['"'+col.name.lower()+'"' for col in row.columns]
    columns_list_str = ','.join(columns_list)
    columns_values_list = ["'"+str(col.value)+"'" for col in row.columns]
    columns_values_list_str = ','.join(columns_values_list)
    sql = 'INSERT INTO {} ({})\n'.format(tablename, columns_list_str)
    sql += 'VALUES ({})\n'.format(columns_values_list_str)
    return sql

def insert_rows_sql(rows: list[DataRow], tablename, table_structure:XsdObject):
    columns_list = ['"'+col.name.lower()+'"' for col in table_structure.attributes]
    columns_list_str = ','.join(columns_list)
    sql = 'INSERT INTO {} ({})\n'.format(tablename, columns_list_str)
    sql += 'VALUES ('
    for row in rows:
        sorted_row = []
        for col in table_structure.attributes:
            pass




