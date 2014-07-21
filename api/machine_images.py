import run, sys
from math import ceil
from flask import jsonify, request
from sqlalchemy import func, desc

#####  Machine Images Related API calls

class MachineImages(run.restful.Resource):
  '''
  Returns a list of all available machine images.
  '''
  def get(self):
    if 'page' in request.args:
      page = int(request.args['page'])
    else:
      page = 1
    q = run.session.query(run.machine_image, run.machine_image_meta_data)\
        .outerjoin(run.machine_image_meta_data, run.machine_image.c.machine_image_id == run.machine_image_meta_data.c.machine_image)
    per_page = 50
    total_count = q.count()
    total_pages = int(ceil(total_count / float(per_page)))
    offset = (per_page * page)
    q = q.limit(per_page).offset(offset).all()
    run.session.close()
    return jsonify(page=page,per_page=per_page,total_pages=total_pages,results=q)

run.api.add_resource(MachineImages, '/api/machine_images')

class TopMachineImages(run.restful.Resource):
  '''
  Returns a list of the top machine images. Defaults to 10
  '''
  def get(self):
    if 'limit' in request.args:
      limit = int(request.args['limit'])
    else:
      limit = 10
    q = run.session.query(run.machine_image.c.machine_image_id, run.machine_image_meta_data.c.name, func.count(run.machine_image_meta_data.c.machine_image).label('count'))\
        .outerjoin(run.server, run.machine_image.c.machine_image_id == run.server.c.machine_image)\
        .outerjoin(run.machine_image_meta_data, run.machine_image.c.machine_image_id == run.machine_image_meta_data.c.machine_image)\
        .group_by(run.machine_image_meta_data.c.name)\
        .order_by(desc(func.count(run.machine_image_meta_data.c.name)))\
        .limit(limit).all()
    run.session.close()
    return jsonify(results=q)

run.api.add_resource(TopMachineImages, '/api/top_machine_images')
