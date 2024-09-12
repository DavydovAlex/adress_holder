from  xml.dom import minidom

def read_xml(path):
    with open(path, encoding='utf-8') as xml_file:
        dom = minidom.parse(xml_file)
        for element in dom.getElementsByTagName('HOUSETYPES')



if __name__ == '__main__':
    read_xml(r'D:\Поиск адресов\Новая папка\AS_ADDHOUSE_TYPES_20240905_28544975-afc8-428e-9bf9-77562dbf3999.XML')
