import run, sys
from math import ceil
from flask import jsonify, request
from sqlalchemy import func, desc

#####  Budget Code Related API calls

class Budgets(run.restful.Resource):
  """ Returns a list of budget codes.

  Args:
    activeOnly (boolean) - optional: expects true (defaults to false)
    page (int): from 1 to 'n' (default: 1)

  Examples:
    /api/budgets?activeOnly=true

  Returns:
    JSON Formatted response:

      {
        page: 3,
        total_count: 6629,
        per_page: 50,
        total_pages: 133,
        results: [
          {
            customer: 500,
            hard_quota: null,
            description: "Default Billing Code",
            finance_code: "DEF",
            billing_code_id: 3901,
            soft_quota: null,
            active: "Y",
            name: "Default"
          },
          {
            customer: 300,
            hard_quota: 2000,
            description: "Another Budget Code",
            finance_code: "ABC",
            billing_code_id: 3902,
            soft_quota: 1000,
            active: "Y",
            name: "Another Budget Code"
          },
          ...

  """
  def get(self):
    q = run.session.query(run.billing_code.c.billing_code_id, run.billing_code.c.name, run.billing_code.c.finance_code, run.billing_code.c.soft_quota, run.billing_code.c.hard_quota, run.billing_code.c.active)

    if 'page' in request.args:
      page = int(request.args['page'])
    else:
      page = 1

    if 'activeOnly' in request.args:
      if request.args['activeOnly']:
        q = q.filter(run.billing_code.c.active == 'Y')

    per_page = 50
    total_count = q.count()
    total_pages = int(ceil(total_count / float(per_page)))
    offset = (per_page * page)

    return jsonify(page=page,per_page=per_page,total_count=total_count,total_pages=total_pages,results=q.limit(per_page).offset(offset).all())

run.api.add_resource(Budgets, '/api/budgets')

class ServersByBudget(run.restful.Resource):
  ''' Count of servers by budget code.

  Args:
    activeOnly (boolean) - optional: expects true or false (defaults to false)

  Examples:
    /api/budgets?activeOnly=true - returns active = 'Y' budget codes

  Returns:
    JSON Formatted response:

      {
        results: [
          {
            count: 10429,
            name: "Budget #1"
          },
          {
            count: 8539,
            name: "Budget #2"
          },
          {
            count: 7479,
            name: "Budget #3"
          },
          ...

  '''
  def get(self):
    q = run.session.query(run.billing_code.c.name,\
        func.count(run.billing_code.c.billing_code_id).label('count'))\
        .outerjoin(run.server, run.billing_code.c.billing_code_id == run.server.c.budget)

    if 'activeOnly' in request.args:
      q = q.filter(run.billing_code.c.active == 'Y')

    q = q.group_by(run.server.c.budget)\
        .order_by(desc(func.count(run.billing_code.c.billing_code_id).label('count')))\
        .all()
    run.session.close()
    return jsonify(results=q)

run.api.add_resource(ServersByBudget, '/api/servers_by_budget')
