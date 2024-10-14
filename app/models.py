from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, Integer, String, BigInteger, Date, Boolean
from extract.extractor import ExtractedObject, Directory
from xsdreader.xsd import Xsd
from pathlib import Path
from xsdreader.xml import DataRow,DataColumn




class Base(DeclarativeBase): pass


class Assotiator:
    _extracted_object: ExtractedObject
    _dirname: str

    @classmethod
    def associate_dir(cls, extracted_obj: ExtractedObject, dirname: str):
        cls._dirname = dirname
        cls._extracted_object = extracted_obj

    @classmethod
    def get_directory(cls) -> Directory:
        return cls._extracted_object.get_directory_by_name(cls._dirname)

    @classmethod
    def get_models(cls):
        return Base.__subclasses__()

class Initiator:

    @classmethod
    def initialize(cls, rows: DataRow| list[DataRow]):
        if isinstance(rows, list):
            model_objects = []
            for row in rows:
                model_objects.append(cls(**row.to_dict()))
            return model_objects
        else:
            return [cls(**rows.to_dict())]


class AddressObject(Base, Assotiator, Initiator):
    __tablename__ = 'addr_obj'

    id = Column(name='id', type_=BigInteger, primary_key=True, quote=True)
    objectid = Column(name='objectid', type_=BigInteger, quote=True)
    objectguid = Column(name='objectguid', type_=String(36), quote=True)
    changeid = Column(name='changeid', type_=BigInteger, quote=True)
    name = Column(name='name', type_=String(250), quote=True)
    typename = Column(name='typename', type_=String(50), quote=True)
    level = Column(name='level', type_=String(50), quote=True)
    opertypeid = Column(name='opertypeid', type_=Integer, quote=True)
    previd = Column(name='previd', type_=BigInteger, quote=True)
    nextid = Column(name='nextid', type_=BigInteger, quote=True)
    updatedate = Column(name='updatedate', type_=Date, quote=True)
    startdate = Column(name='startdate', type_=Date, quote=True)
    enddate = Column(name='enddate', type_=Date, quote=True)
    isactual = Column(name='isactual', type_=Integer, quote=True)
    isactive = Column(name='isactive', type_=Integer, quote=True)

class AddressTypes(Base, Assotiator, Initiator):
    __tablename__ = 'addr_obj_types'

    id = Column(name='id', type_=Integer, primary_key=True, quote=True)
    level = Column(name='level', type_=Integer, quote=True)
    shortname = Column(name='shortname', type_=String(50), quote=True)
    name = Column(name='name', type_=String(250), quote=True)
    desc = Column(name='desc', type_=String(250), quote=True)
    updatedate = Column(name='updatedate', type_=Date, quote=True)
    startdate = Column(name='startdate', type_=Date, quote=True)
    enddate = Column(name='enddate', type_=Date, quote=True)
    isactive = Column(name='isactive', type_=Boolean, quote=True)

class AddressParams(Base, Assotiator, Initiator):
    __tablename__ = 'addr_obj_params'

    id = Column(name='id', type_=BigInteger, primary_key=True, quote=True)
    objectid = Column(name='objectid', type_=BigInteger, quote=True)
    changeid = Column(name='changeid', type_=BigInteger, quote=True)
    changeidend = Column(name='changeidend', type_=BigInteger, quote=True)
    typeid = Column(name='typeid', type_=Integer, quote=True)
    value = Column(name='value', type_=String(8000), quote=True)
    updatedate = Column(name='updatedate', type_=Date, quote=True)
    startdate = Column(name='startdate', type_=Date, quote=True)
    enddate = Column(name='enddate', type_=Date, quote=True)

class AdmHierarchy(Base, Assotiator, Initiator):
    __tablename__ = 'adm_hierarchy'

    id = Column(name='id', type_=BigInteger, primary_key=True, quote=True)
    objectid = Column(name='objectid', type_=BigInteger, quote=True)
    parentobjid = Column(name='parentobjid', type_=BigInteger, quote=True)
    changeid = Column(name='changeid', type_=BigInteger, quote=True)
    regioncode = Column(name='regioncode', type_=String(4), quote=True)
    areacode = Column(name='areacode', type_=String(4), quote=True)
    citycode = Column(name='citycode', type_=String(4), quote=True)
    placecode = Column(name='placecode', type_=String(4), quote=True)
    plancode = Column(name='plancode', type_=String(4), quote=True)
    streetcode = Column(name='streetcode', type_=String(4), quote=True)
    previd = Column(name='previd', type_=BigInteger, quote=True)
    nextid = Column(name='nextid', type_=BigInteger, quote=True)
    updatedate = Column(name='updatedate', type_=Date, quote=True)
    startdate = Column(name='startdate', type_=Date, quote=True)
    enddate = Column(name='enddate', type_=Date, quote=True)
    isactive = Column(name='isactive', type_=Integer, quote=True)
    path = Column(name='path', type_=String, quote=True)


class ObjectLevels(Base, Assotiator, Initiator):
    __tablename__ = 'object_levels'

    level = Column(name='level', type_=Integer, primary_key=True, quote=True)
    name = Column(name='name', type_=String(250), quote=True)
    shortname = Column(name='shortname', type_=String(50), quote=True)
    updatedate = Column(name='updatedate', type_=Date, quote=True)
    startdate = Column(name='startdate', type_=Date, quote=True)
    enddate = Column(name='enddate', type_=Date, quote=True)
    isactive = Column(name='isactive', type_=Boolean, quote=True)


class ParamTypes(Base, Assotiator, Initiator):
    __tablename__ = 'param_types'

    id = Column(name='id', type_=Integer, primary_key=True, quote=True)
    name = Column(name='name', type_=String(50), quote=True)
    code = Column(name='code', type_=String(50), quote=True)
    desc = Column(name='desc', type_=String(120), quote=True)
    updatedate = Column(name='updatedate', type_=Date, quote=True)
    startdate = Column(name='startdate', type_=Date, quote=True)
    enddate = Column(name='enddate', type_=Date, quote=True)
    isactive = Column(name='isactive', type_=Boolean, quote=True)



