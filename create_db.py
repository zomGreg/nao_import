from sqlalchemy import create_engine, schema, types
from sqlalchemy import MetaData,Column,Table,ForeignKey
from sqlalchemy import Integer,String,Date
import datetime
from sqlalchemy import orm, func, select
from sqlalchemy.sql import and_, or_, not_

metadata=schema.MetaData()
engine=create_engine('sqlite:///nao.db', echo=False)
metadata.bind=engine

games=Table('games',metadata,
            schema.Column('id', types.Integer, schema.Sequence('game_id', optional=True), primary_key=True),
            Column('align0',String(3)),
            Column('deathlev', Integer),
            Column('uid',Integer),
            Column('deaths',Integer),
            Column('turns',Integer),
            Column('points',Integer),
            Column('death',String(250)),
            Column('realtime',Integer),
            Column('version',String(7)),
            Column('role',String(3)),
            Column('conduct',Integer),
            Column('gender0',String(3)),
            Column('deathdate',Date),
            Column('hp',Integer),
            Column('achieve',Integer),
            Column('gamedelta',Integer),
            Column('maxlvl',Integer),
            Column('maxhp',Integer),
            Column('endtime',Date),
            Column('nachieves',Integer),
            Column('nconducts',Integer),
            Column('name',String(64)),
            Column('gender',String(3)),
            Column('align',String(3)),
            Column('birthdate',Date),
            Column('race',String(3)),
            Column('flags',Integer),
            Column('starttime',Date),
            Column('deathdnum',Integer)
)

# Need this if you're going to create from scratch.
#games.create()

class Games(object):
    pass

def load_game(game_dict):
    connection=engine.connect()
    ins=games.insert(game_dict)
    connection.execute(ins)
