from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, Integer, String, BigInteger, Date
from extract.extractor import ExtractedObject, Directory
from xsdreader.xsd import Xsd
from pathlib import Path




class Base(DeclarativeBase):
    _extracted_object: ExtractedObject
    _dirname: str

    @classmethod
    def associate_dir(cls, extracted_obj: ExtractedObject, dirname: str):
        cls._dirname = dirname
        cls._extracted_object = extracted_obj

    @classmethod
    def get_directory(cls):
        return cls._dirname


    @classmethod
    def get_models(cls):
        return Base.__subclasses__()

class AddressObject(Base):
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

class AddressTypes(Base):
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



