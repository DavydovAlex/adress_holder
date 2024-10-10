__all__ = ['QueryGenerator']

from .attribute import Attribute, ABoolean, ALong, AInteger, AString, ADate
from .xsd import Xsd
from .xml import DataRow


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
    def create_table(xsd_obj: Xsd, tablename: str | None = None) -> str:
        sql = 'CREATE TABLE {} (\n'.format(tablename if tablename is not None else xsd_obj.name)
        for attribute in xsd_obj.attributes:
            column_datatype = QueryGenerator.__get_db_type(attribute)
            sql += '"{}" {}{},\n'.format(attribute.name.lower(),
                                         column_datatype,
                                         '({})'.format(attribute.length) if attribute.length is not None else '')
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


    @staticmethod
    def __get_names_string(row: DataRow):
        columns_list = ['"' + col.name.lower() + '"' for col in row.columns]
        return ','.join(columns_list)

    @staticmethod
    def __get_values_string(row: DataRow):
        values_list = []
        for col in row.columns:
            if col.value is not None:
                values_list.append("'" + str(col.value) + "'")
            else:
                values_list.append("null")
        return ','.join(values_list)

    @staticmethod
    def insert_row(row: DataRow, tablename):
        return QueryGenerator.insert_rows([row])

    @staticmethod
    def insert_rows(rows: list[DataRow], tablename):
        if len(rows) == 0:
            raise Exception('Список не может быть пустым')
        columns_list_str = QueryGenerator.__get_names_string(rows[0])
        sql = 'INSERT INTO {} ({}) VALUES\n'.format(tablename, columns_list_str)
        for row in rows:
            sql += '(' + QueryGenerator.__get_values_string(row) + '),\n'
        sql = sql[0:-2] + ';\n'
        return sql



