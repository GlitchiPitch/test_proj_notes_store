from sqlalchemy import MetaData, Column, Integer, String
from sqlalchemy.orm import DeclarativeBase, declared_attr

class Base(DeclarativeBase):
    metadata = MetaData()
    @declared_attr
    def __tablename__(cls) -> str:
        return f'{cls.__name__.lower()}s'

class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)

class Note(Base):
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    owner_id = Column(Integer, nullable=False)
