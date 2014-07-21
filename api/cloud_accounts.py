import run, sys
from math import ceil
from flask import jsonify, request
from sqlalchemy import func, desc

#####  Cloud Accounts Related API calls

class CloudAccounts(run.restful.Resource):
  ''' Returns a list of all servers regardless of state.

  Args:
    activeOnly (boolean) - optional: expects true (defaults to false)
    page (int): from 1 to 'n' (default: 1)

  Examples:
    /api/cloud_accounts?activeOnly=true

  Returns:
    JSON formatted response:

  '''
  def get(self):
    ''' TODO:  Limit fields to only required. '''
    q = run.session.query(run.cloud_account)

    if 'page' in request.args:
      page = int(request.args['page'])
    else:
      page = 1

    if 'activeOnly' in request.args:
      if request.args['activeOnly']:
        q = q.filter(run.cloud_account.c.active == 'Y')

    per_page = 50
    total_count = q.count()
    total_pages = int(ceil(total_count / float(per_page)))
    offset = (per_page * page)

    return jsonify(page=page,per_page=per_page,total_count=total_count,total_pages=total_pages,results=q.limit(per_page).offset(offset).all())

run.api.add_resource(CloudAccounts, '/api/cloud_accounts')

class AccountsWithServersTerminated(run.restful.Resource):
  '''
  Returns a list of accounts, with the number of servers with state=TERMINATED in each account
  The dataset returned by this query is suitable for display in a bar chart.
  '''
  def get(self):
    q = run.session.query(func.count(run.cloud_account.c).label('count'), run.customer_billing.c.account_name)\
        .select_from(run.cloud_account)\
        .outerjoin(run.customer_billing, run.customer_billing.c.customer_billing_id == run.cloud_account.c.billing)\
        .outerjoin(run.server, run.server.c.account == run.cloud_account.c.cloud_account_id)\
        .outerjoin(run.cached_server, run.cached_server.c.server_id == run.server.c.server_id)\
        .filter(run.cached_server.c.current_state == 'TERMINATED')\
        .group_by(run.cached_server.c.current_state, run.customer_billing.c.account_name).order_by(desc(func.count(run.cloud_account.c)))\
        .all()
    run.session.close()
    return jsonify(results=q)

run.api.add_resource(AccountsWithServersTerminated, '/api/accounts_with_servers_terminated')

class AccountsWithServersRunning(run.restful.Resource):
  '''
  Returns a list of accounts, with the number of servers with state=TERMINATED in each account
  The dataset returned by this query is suitable for display in a bar chart.
  '''
  def get(self):
    q = run.session.query(func.count(run.cloud_account.c).label('count'), run.customer_billing.c.account_name)\
        .select_from(run.cloud_account)\
        .outerjoin(run.customer_billing, run.customer_billing.c.customer_billing_id == run.cloud_account.c.billing)\
        .outerjoin(run.server, server.c.account == run.cloud_account.c.cloud_account_id)\
        .outerjoin(run.cached_server, run.cached_server.c.server_id == run.server.c.server_id)\
        .filter(run.cached_server.c.current_state == 'RUNNING')\
        .group_by(run.cached_server.c.current_state, run.customer_billing.c.account_name).order_by(desc(func.count(run.cloud_account.c)))\
        .all()
    run.session.close()
    return jsonify(results=q)

run.api.add_resource(AccountsWithServersRunning, '/api/accounts_with_servers_running')
