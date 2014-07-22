import run
import datetime
from math import ceil
from flask import jsonify, request
from sqlalchemy import func, desc, Integer

#### Namespace /api/games/*

# === /api/games ===

class Servers(run.restful.Resource):
    """
    Returns a list of all servers regardless of state.

    **Args:**

    *state* (**str**) - optional: expects one of RUNNING, TERMINATED, STOPPED (no default)
    *limit* (**int**) - optional: from 1 to 'n' (no default)
    *page* (**int**): from 1 to 'n' (default: 1)

    **Examples:**

    /api/servers?state=RUNNING&limit=10
    /api/servers?limit=15
    /api/servers?page=2

    **Returns:**

      {
        state: None,
        per_page: 50,
        total_count: 12515,
        total_pages: 1436,
        page: 1,
        results: [
            {
              clonable: "N",
              termination_timestamp: 1327615801646,
              last_stop_timestamp: null,
              provider_subnet_id: null,
              private_dns_address: "10.35.147.37",
              provider_owner_id: "enstratus_console",
              created_timestamp: 1327076382917,
              provider_product_id: "22",
              provider_data_center_id: "1",
              server_id: 709,
              cloud_id: 20013,
              analytics_enabled: "N",
              platform: "UNKNOWN",
              private_ip_addresses: "10.35.147.37",
              provider_image_id: "692",
              auto_assigned_public_dns_address: null,
              description: "i-31-6345-VM",
              provider_assigned_ip_address_id: null,
              provider_region_id: "1",
              last_modified: 1327615801646,
              name: "AGENTTEST003",
              public_ip_addresses: null,
              current_state: "TERMINATED",
              persistent: "Y",
              architecture: "I64",
              public_dns_address: null,
              provider_server_id: "6345",
              last_start_timestamp: 1327076382917,
              provider_network_id: "204"
            },
          ...
    """
    def get(self):
        q = run.session.query(run.cached_server).order_by(run.cached_server.c.server_id)

        if 'state' in request.args:
            state = request.args['state']
            q = q.filter(run.cached_server.c.current_state == state)
        else:
            state = None

        if 'limit' in request.args:
            limit = int(request.args['limit'])

            return jsonify(results=q.limit(limit).all())
        else:
            if 'page' in request.args:
                page = int(request.args['page'])
            else:
                page = 1

        per_page = 50
        total_count = q.count()
        total_pages = int(ceil(total_count / float(per_page)))
        offset = (per_page * page)
        return jsonify(state=state,
                       page=page,
                       per_page=per_page,
                       total_pages=total_pages,
                       total_count=total_count,
                       results=q.limit(per_page).offset(offset).all())

run.api.add_resource(Servers, '/api/servers')
