from xsdreader.builder import XsdObject, Attribute, ABoolean, ALong, AInteger, AString, ADate
from copy import deepcopy


def _add_db_pg_type(attribute: Attribute):
    extended_attr = deepcopy(attribute)
    if isinstance(attribute, AString):
        extended_attr.db_type = 'VARCHAR'
    elif isinstance(attribute, ALong):
        extended_attr.db_type = 'BIGINT'
    elif isinstance(attribute, AInteger):
        extended_attr.db_type = 'INTEGER'
    elif isinstance(attribute, ABoolean):
        extended_attr.db_type = 'BOOLEAN'
    elif isinstance(attribute, ADate):
        extended_attr.db_type = 'DATE'
    else:
        raise Exception("Не определен тип данных")
    return extended_attr


def create_table_sql(obj: XsdObject, tablename=None):
    sql = 'CREATE TABLE {} (\n'.format(tablename if tablename is not None else obj.name)
    for column in obj.attributes:
        column_ext = _add_db_pg_type(column)
        sql += '"{}" {}{},\n'.format(column_ext.name.lower(),
                                     column_ext.db_type,
                                     '({})'.format(column.length) if column.length is not None else '')
    sql = sql[0:-2] + ');\n'
    return sql


def create_comments_sql(obj: XsdObject, tablename=None):
    if tablename is not None:
        name = tablename
    else:
        name = obj.name
    sql = "comment on table {} is '{}';\n".format(name, obj.comment)
    for column in obj.attributes:
        sql += "comment on column {}.{} is '{}';\n".format(name,
                                                           column.name.lower(),
                                                           column.comment)
    return sql
