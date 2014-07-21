import run, sys
from math import ceil
from flask import jsonify, request
from sqlalchemy import func, desc

#####  Clouds Related API calls

class Clouds(run.restful.Resource):
  ''' Returns a list of clouds.

  Examples:
    /api/clouds

  Returns:
    JSON formatted response:

      {
        results: [
        {
          endpoint: "https://ec2.us-east-1.amazonaws.com,https://ec2.us-west-1.amazonaws.com,https://ec2.eu-west-1.amazonaws.com,https://ec2.ap-southeast-1.amazonaws.com,https://ec2.ap-northeast-1.amazonaws.com",
          delegate: "org.dasein.cloud.aws.AWSCloud",
          cloud_id: 1,
          name: "Amazon Web Services"
        },
        {
          endpoint: "https://auth.api.rackspacecloud.com/v1.0",
          delegate: "org.dasein.cloud.rackspace.RackspaceCloud",
          cloud_id: 2,
          name: "Rackspace (US)"
        },
        ...
      
  '''
  def get(self):
    q = run.session.query(run.cloud.c.cloud_id, run.cloud.c.name, run.cloud.c.endpoint, run.cloud.c.delegate).all()
    run.session.close()
    return jsonify(results=q)

run.api.add_resource(Clouds, '/api/clouds')
