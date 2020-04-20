# coding: utf-8
from sqlalchemy import Column, Integer, MetaData, String, Table
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base

metadata = MetaData()
Base = declarative_base()

t_db_owner = Table(
    'db_owner', metadata,
    Column('token_id', UUID, nullable=False),
    Column('username', String(30), nullable=False),
    Column('password', String(30), nullable=False)
)


t_db_user = Table(
    'db_user', metadata,
    Column('token_id', UUID, nullable=False),
    Column('phone_number', Integer, nullable=False)
)


class Owner(Base):
    __tablename__ = 'db_owner'
    token_id = Column(UUID, primary_key=True)
    username = Column(String(30))
    password = Column(String(30))


class User(Base):
    __tablename__ = 'db_user'
    token_id = Column(UUID, primary_key=True)
    phone_number = Column(Integer)
