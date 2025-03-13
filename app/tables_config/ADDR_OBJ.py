from .table import Column, ColumnCollection, Table

ADDR_OBJ = Table(name='addr_obj',
                 data_file_folder='54',
                 data_file_pattern='^AS_ADDR_OBJ_\d.+\.XML$',
                 comment='Сведения классификатора адресообразующих элементов',
                 columns=ColumnCollection(
                     Column(name='ID',
                            type_='long',
                            comment='Уникальный идентификатор записи. Ключевое поле',
                            primary_key=True,
                            ),
                     Column(name='OBJECTID',
                            type_='long',
                            comment='Глобальный уникальный идентификатор адресного объекта типа INTEGER',
                            ),
                     Column(name='OBJECTGUID',
                            type_='string',
                            comment='Глобальный уникальный идентификатор адресного объекта типа UUID',
                            length=36
                            ),
                     Column(name='CHANGEID',
                            type_='long',
                            comment='ID изменившей транзакции',
                            ),
                     Column(name='NAME',
                            type_='string',
                            comment='Наименование',
                            length=250
                            ),
                     Column(name='TYPENAME',
                            type_='string',
                            comment='Краткое наименование типа объекта',
                            length=50
                            ),
                     Column(name='LEVEL',
                            type_='string',
                            comment='Уровень адресного объекта',
                            length=10,
                            db_name='object_level'
                            ),
                     Column(name='OPERTYPEID',
                            type_='integer',
                            comment='Статус действия над записью – причина появления записи',
                            ),
                     Column(name='PREVID',
                            type_='long',
                            comment='Идентификатор записи связывания с предыдущей исторической записью',
                            is_empty=True,
                            ),
                     Column(name='NEXTID',
                            type_='long',
                            comment='Идентификатор записи связывания с последующей исторической записью',
                            is_empty=True,
                            ),
                     Column(name='UPDATEDATE',
                            type_='date',
                            comment='Дата внесения (обновления) записи',
                            ),
                     Column(name='STARTDATE',
                            type_='date',
                            comment='Начало действия записи',
                            ),
                     Column(name='ENDDATE',
                            type_='date',
                            comment='Окончание действия записи',
                            ),
                     Column(name='ISACTUAL',
                            type_='integer',
                            comment='Статус актуальности адресного объекта ФИАС',
                            ),
                     Column(name='ISACTIVE',
                            type_='integer',
                            comment='Признак действующего адресного объекта',
                            )
                    )
                 )
