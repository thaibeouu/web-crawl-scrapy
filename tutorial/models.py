from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL

import settings

DeclarativeBase = declarative_base()


def db_connect():
    return create_engine(URL(**settings.DATABASE))


def create_items_table(engine):
    DeclarativeBase.metadata.create_all(engine)


class Items(DeclarativeBase):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True)
    title = Column('title', String)
    price = Column('price', String, nullable=True)
    location = Column('location', String, nullable=True)
    date = Column('date', DateTime)
    time = Column('time', DateTime, nullable=True)
