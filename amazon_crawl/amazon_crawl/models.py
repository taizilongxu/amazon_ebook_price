#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL
import datetime

import settings


DeclarativeBase = declarative_base()


def db_connect():
    """
    Performs database connection using database settings from settings.py.
    Returns sqlalchemy engine instance
    """
    print URL(**settings.DATABASE)
    return create_engine(URL(**settings.DATABASE))


def create_table(engine):
    """"""
    DeclarativeBase.metadata.create_all(engine)


class Books(DeclarativeBase):
    """Sqlalchemy deals model"""
    __tablename__ = "books"

    book_id = Column('book_id', String, primary_key=True)
    name = Column('name', String)
    author = Column('author', String)
    public_date = Column('public_date', String, nullable=True)
    create_date = Column('create_date', DateTime, default=datetime.datetime.utcnow)


class Info(DeclarativeBase):
    """Sqlalchemy deals model"""
    __tablename__ = "info"

    id = Column(Integer, primary_key=True)
    book_id = Column('book_id', String)
    price = Column('price', Float, nullable=True)
    comment_num = Column('comment_num', Integer, nullable=True)
    star = Column('star', Float)
    create_date = Column('create_date', DateTime, default=datetime.datetime.utcnow)
