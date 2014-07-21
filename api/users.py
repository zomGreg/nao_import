import run, sys
from math import ceil
from flask import jsonify, request
from sqlalchemy import func, desc

#####  User Related API calls

class ActiveUsersCount(run.restful.Resource):
  '''
  Returns a count of active users
  '''
  def get(self):
    q = run.session.query(func.count(run.enstratus_user.c.enstratus_user_id).label('count')).all()
    run.session.close()
    return jsonify(results=q)

run.api.add_resource(ActiveUsersCount, '/api/active_users_count')
