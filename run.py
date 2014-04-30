from sqlalchemy import create_engine, schema, types
from sqlalchemy import MetaData,Column,Table,ForeignKey
from flask import jsonify, request
from sqlalchemy import Integer,String,Date
import datetime
from sqlalchemy import orm, func, select
from sqlalchemy.sql import and_, or_, not_
from sqlalchemy.orm import sessionmaker

metadata=schema.MetaData()
engine=create_engine('sqlite:///nao.db', echo=False)
metadata.bind=engine
session = sessionmaker(bind=engine)()

games=Table('games', metadata, autoload=True)

class Games(object):
    pass

orm.mapper(Games,games)
sm=orm.sessionmaker(bind=engine, autoflush=True, autocommit=False, expire_on_commit=True)
session=orm.scoped_session(sm)

test=session.query(func.max(Games.points))
print test.all()
