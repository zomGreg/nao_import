import run
import datetime
from math import ceil
from flask import jsonify, request
from sqlalchemy import func, desc, Integer, text

## Server Related API calls

class Games(run.restful.Resource):
    """
    Games
    """
    def get(self):
        q = run.session.query(func.count(run.nethack_games.c.id).label('count')).all()
        run.session.close()
        return jsonify(results=q)

run.api.add_resource(Games, '/api/total_games')

class MaxPoints(run.restful.Resource):
    """
    Games
    """
    def get(self):
        q = run.session.query(func.max(run.nethack_games.c.points).label('points')).all()
        run.session.close()
        return jsonify(results=q)

run.api.add_resource(MaxPoints, '/api/max_points')
