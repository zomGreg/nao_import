import run, sys
from math import ceil
from sqlalchemy.ext.serializer import loads, dumps
from sqlalchemy import func, desc

def test_query():
    q = run.session.query(func.count(run.games.c.points))

    q=run.session.query(run.games.c.name)

    return q

print test_query()
