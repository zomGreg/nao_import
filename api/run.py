import os, functions
from flask import Flask, jsonify, request, render_template
from flask.ext import restful
from sqlalchemy import Table, create_engine, schema, func, desc
from sqlalchemy.orm import sessionmaker

app = Flask(__name__, template_folder='../app', static_folder='../app/static')
app.debug = True
api = restful.Api(app)
db_user = os.environ.get('DBUSER')
db_pass = os.environ.get('DBPASS')
db_host = os.environ.get('DBHOST')
db_name = os.environ.get('DBNAME')
sql_creds = db_user

if db_pass is not None:
    sql_creds += ":" + db_pass

metadata = schema.MetaData()
engine = create_engine('mysql://'+sql_creds+'@'+db_host+'/'+db_name, pool_recycle=360, convert_unicode=True, echo=False)
metadata.bind = engine
session = sessionmaker(bind=engine)()
server = Table('server', metadata, autoload=True)
cached_server = Table('cached_server', metadata, autoload=True)
server_request = Table('server_request', metadata, autoload=True)
server_change = Table('server_change', metadata, autoload=True)
#server_agent = Table('server_agent', metadata, autoload=True)
#server_automation = Table('server_automation', metadata, autoload=True)
#agent_item = Table('agent_item', metadata, autoload=True)
provider_region = Table('provider_region', metadata, autoload=True)
cloud = Table('cloud', metadata, autoload=True)
person = Table('person', metadata, autoload=True)
enstratus_user = Table('enstratus_user', metadata, autoload=True)
billing_code = Table('billing_code', metadata, autoload=True)
enstratus_job = Table('enstratus_job', metadata, autoload=True)
machine_image = Table('machine_image', metadata, autoload=True)
machine_image_meta_data = Table('machine_image_meta_data', metadata, autoload=True)
customer_billing = Table('customer_billing', metadata, autoload=True)
cloud_account = Table('cloud_account', metadata, autoload=True)

@app.route('/servers')
@app.route('/jobs')
@app.route('/report')
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/resources/server/<int:server_id>')
def resources_server(server_id):
    return render_template('index.html')

import servers
import budgets
import jobs
import machine_images
import cloud_accounts
import clouds
import users
