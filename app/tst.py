# from tables_config.table import Table
from tables_config.ADDR_OBJ import ADDR_OBJ
from tables_config.archive import Archive

arc = Archive(r'D:\gar\gar_xml.zip')
ADDR_OBJ.read_data(arc.get_data(ADDR_OBJ.data_file_pattern,
                                ADDR_OBJ.data_file_folder))
# print(ADDR_OBJ.name)
# print(ADDR_OBJ.comment)
# print(ADDR_OBJ.data_file_folder)
# print(ADDR_OBJ.data_file_pattern)
# print(ADDR_OBJ.columns['ID'].db_type)
print(len(ADDR_OBJ.columns))
print(ADDR_OBJ.get_create_table_sql())
print(ADDR_OBJ.get_create_comments_sql())
print('ID' in ADDR_OBJ.columns)

# for col in ADDR_OBJ.columns:
#     print(col.name)

# print(type(None))
# t = Table('ADDR_OBJ')
# print(t.source_file_pattern)
# print(t.folder)
# print(t.db_tablename)
# print(t.description)
