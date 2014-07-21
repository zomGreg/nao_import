import run, sys
from math import ceil
from flask import jsonify, request
from sqlalchemy import func, desc

#####  Job Related API calls

class Jobs(run.restful.Resource):
  '''
  Returns a list of all available jobs.
  '''
  def get(self):
    q = run.session.query(run.enstratus_job.c.job_id, run.enstratus_job.c.description,\
        ((run.enstratus_job.c.end_timestamp-run.enstratus_job.c.start_timestamp)/1000).label('seconds_to_complete'),\
        run.enstratus_job.c.job_status,\
        (func.from_unixtime(run.enstratus_job.c.start_timestamp/1000, '%Y-%m-%d %h:%i:%s')).label('start_date'),\
        (func.from_unixtime(run.enstratus_job.c.end_timestamp/1000, '%Y-%m-%d %h:%i:%s')).label('end_date'))

    if 'limit' in request.args:
      limit = int(request.args['limit'])

      return jsonify(results=q.order_by(run.enstratus_job.c.start_timestamp).limit(limit).all())
    else:
      if 'page' in request.args:
        page = int(request.args['page'])
      else:
        page = 1

      per_page = 50
      total_count = q.count()
      total_pages = int(ceil(total_count / float(per_page)))
      offset = (per_page * page)
      q = q.order_by(run.enstratus_job.c.start_timestamp).limit(per_page).offset(offset).all()
      run.session.close()
      return jsonify(page=page,per_page=per_page,total_pages=total_pages,results=q)

run.api.add_resource(Jobs, '/api/jobs')
