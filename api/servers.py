import run
import datetime
from math import ceil
from flask import jsonify, request
from sqlalchemy import func, desc, Integer

## Server Related API calls

#### Namespace /api/server/*


# === /api/servers ===


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


# === /api/server_action ===


class ServerAction(run.restful.Resource):
    """
    Returns a summary of the number of server events (CREATE, UPDATE, and DELETE) grouped by month.

    **Args**:

    *action* (**str**): expects one of CREATE, UPDATE, or DELETE (no default)
    *start* (**date**): date in the format of YYYY-MM
    *end* (**date**): date in the format of YYYY-MM
    *days* (**int**): expects integer 'n' (example: 30 means the last 30 days)
    *months* (**int**): expects integer 'n'

    **Examples:**

    /api/server_action?action=CREATE
    /api/server_action?action=DELETE&start=2012-07&end=2013-07

    **Returns:**

    {
        action: "CREATE",
        results: [
            {
                count: 50,
                d: 1329850610
            },
            ...
    """
    def get(self):
        if 'action' in request.args:
            q = run.session.query((run.server_request.c.event_timestamp).label('d'),
                                  func.sum(func.IF(run.server_request.c.event_type == request.args['action'], 1, 0))
                                  .label('count'))\
                .outerjoin(run.server_change, run.server_request.c.event_id == run.server_change.c.request)

            if 'start' in request.args:
                q = q.filter(func.from_unixtime(run.server_request.c.event_timestamp/1000,'%Y-%m-%d')
                             >= request.args['start'])

            if 'end' in request.args:
                q = q.filter(func.from_unixtime(run.server_request.c.event_timestamp/1000,'%Y-%m-%d')
                             <= request.args['end'])

            if 'days' in request.args:
                start_date = datetime.datetime.now() + datetime.timedelta(-int(request.args['days']))
                q = q.filter(func.from_unixtime(run.server_request.c.event_timestamp / 1000, '%Y-%m-%d')
                             .between(start_date.strftime('%Y-%m-%d'), datetime.datetime.now().strftime('%Y-%m-%d')))

            q = q.filter(run.server_change.c.external == 'N')\
                .group_by(func.from_unixtime(run.server_request.c.event_timestamp / 1000, '%Y-%m-%d'))\
                .order_by(func.from_unixtime(run.server_request.c.event_timestamp / 1000, '%Y-%m-%d'))

            if 'months' in request.args:
                q = q.limit(int(request.args['months']))

            return jsonify(action=request.args['action'],
                           results=run.functions.flatten_json(q.all()))

        else:
            return jsonify(error="requires action of CREATE, UPDATE, or DELETE")

run.api.add_resource(ServerAction, '/api/server_action')


# === /api/server_state_summary ===


class ServerStateSummary(run.restful.Resource):
    """
    Returns a count of servers by state.

    Args:
    none

    Examples:
    /api/server_state_summary

    Returns:
    JSON Formatted response:

    {
      results: [
        {
          y: 5,
          key: "STOPPING"
        },
        {
          y: 35,
          key: "PAUSED"
        },
        {
          y: 578,
          key: "STOPPED"
        },
        {
          y: 2254,
          key: "RUNNING"
        },
        {
          y: 68910,
          key: "TERMINATED"
        }
      ]
    }
    """
    def get(self):
        q = run.session.query(func.count(run.cached_server.c.current_state).label('y'),
                              run.cached_server.c.current_state.label('key'))\
            .group_by(run.cached_server.c.current_state).order_by(func.count(run.cached_server.c.current_state)).all()
        return jsonify(results=q)

run.api.add_resource(ServerStateSummary, '/api/server_state_summary')


# === /api/server_owned_count ===


class ServerOwnedCount(run.restful.Resource):
    """
    Returns the total number of servers with an owner.
    """
    def get(self):
        q = run.session.query(func.count(run.server.c).label('count'))\
            .filter(run.server.c.server_id != None).all()
        return jsonify(results=q)

run.api.add_resource(ServerOwnedCount, '/api/server_owned_count')


# === /api/server_action_count_by_month ===


class ServerActionGrouped(run.restful.Resource):
    """
    Returns a summary of the number of server events (CREATE and DELETE) grouped by month.

    Examples:
    /api/server_action_grouped?start=2012-03
    /api/server_action_grouped?end=2012-11
    /api/server_action_grouped?start=2012-03&end=2012-11
    """
    def get(self):
        q = run.session.query(func.from_unixtime(run.server_request.c.event_timestamp / 1000, '%Y-%m-%d %T')
                              .label('d'),
                              func.sum(func.IF(run.server_request.c.event_type == 'CREATE', 1, 0))
                              .label('launches'),
                              func.sum(func.IF(run.server_request.c.event_type == 'DELETE', 1, 0))
                              .label('terminations'))\
            .outerjoin(run.server_change, run.server_request.c.event_id == run.server_change.c.request)

        if 'start' in request.args:
            q = q.filter(func.from_unixtime(run.server_request.c.event_timestamp / 1000, '%Y-%m')
                         >= request.args['start'])
        else:
            last_year = datetime.datetime.now() - datetime.timedelta(365.24)
            q = q.filter(func.from_unixtime(run.server_request.c.event_timestamp / 1000, '%Y-%m-%d')
                         >= last_year.strftime('%Y-%m-%d'))

        if 'end' in request.args:
            q = q.filter(func.from_unixtime(run.server_request.c.event_timestamp / 1000, '%Y-%m')
                         <= request.args['end'])

        q = q.filter(run.server_change.c.external == 'N')\
            .group_by(func.from_unixtime(run.server_request.c.event_timestamp / 1000, '%Y-%m-%d'))\
            .order_by(func.from_unixtime(run.server_request.c.event_timestamp / 1000, '%Y-%m-%d'))

        return jsonify(results=q.all())

run.api.add_resource(ServerActionGrouped, '/api/server_action_grouped')


# === /api/server_action_count_by_day ===


class ServerActionCountByDay(run.restful.Resource):
    """
    Returns a summary of the number of server events (CREATE, UPDATE, and DELETE) grouped by day.

    Examples:
    /api/server_action_count_by_day?days=30 (list in ascending order)
    """
    def get(self):
        q = run.session.query(func.from_unixtime(run.server_request.c.event_timestamp/1000,'%Y-%m-%d').label('d'),
            func.sum(func.IF(run.server_request.c.event_type == 'CREATE', 1, 0)).label('launches'),
            func.sum(func.IF(run.server_request.c.event_type == 'UPDATE', 1, 0)).label('updates'),
            func.sum(func.IF(run.server_request.c.event_type == 'DELETE', 1, 0)).label('terminations'))

        if 'days' in request.args:
            start_date = datetime.datetime.now() + datetime.timedelta(-int(request.args['days']))

            q = q.filter(func.from_unixtime(run.server_request.c.event_timestamp/1000,'%Y-%m-%d')
                         .between(start_date.strftime('%Y-%m-%d'), datetime.datetime.now().strftime('%Y-%m-%d')))

        q = q.group_by(func.from_unixtime(run.server_request.c.event_timestamp/1000,'%Y-%m-%d'))\
            .order_by(func.from_unixtime(run.server_request.c.event_timestamp/1000,'%Y-%m-%d')).all()

        return jsonify(results=q)

run.api.add_resource(ServerActionCountByDay, '/api/server_action_count_by_day')


# === /api/server_event_count ===


class ServerEventCount(run.restful.Resource):
    """
    Returns the sum of the number of servers along with event type
    """
    def get(self):
        q = run.session.query(func.count(run.server_request.c.event_id).label('count'), run.server_request.c.event_type)\
            .group_by(run.server_request.c.event_type).all()
        return jsonify(results=q)

run.api.add_resource(ServerEventCount, '/api/server_event_count')


# === /api/server_event_count ===


class ServerAverageLifetime(run.restful.Resource):
    """
    Returns a time-ordered monthly summary list of server "lifetime" in
    hours as determined by the termination_timestamp - creation_timestamp values found in cached_server
    """
    def get(self):
        q = run.session.query(func.count(run.cached_server.c.server_id).label('count'),
                              func.from_unixtime(run.cached_server.c.created_timestamp/1000,'%Y-%m').label('created'),
                              ((((run.cached_server.c.termination_timestamp-run.cached_server.c.created_timestamp)/1000)/60)/60).label('life_span_hours'))\
            .filter(run.cached_server.c.termination_timestamp is not None)\
            .group_by(func.from_unixtime(run.cached_server.c.created_timestamp/1000,'%Y-%m'))\
            .order_by(func.from_unixtime(run.cached_server.c.created_timestamp/1000,'%Y-%m')).all()

        return jsonify(results=q)

run.api.add_resource(ServerAverageLifetime, '/api/server_average_lifetime')


# === /api/server_earliest_launch_request ===


class ServerEarliestLaunchRequest(run.restful.Resource):
    """
    Returns a long value of the earliest launch request timestamp.
    """
    def get(self):
        q = run.session.query(func.min(run.server_request.c.event_timestamp/1000).label('earliest_server_launch')).all()
        return jsonify(results=q)

run.api.add_resource(ServerEarliestLaunchRequest, '/api/server_earliest_launch_request')


# === /api/server_latest_launch_request ===


class ServerLatestLaunchRequest(run.restful.Resource):
    """
    Returns a long value of the latest launch request timestamp.
    """
    def get(self):
        q = run.session.query(func.max(run.server_request.c.event_timestamp/1000).label('latest_server_launch')).all()
        return jsonify(results=q)

run.api.add_resource(ServerLatestLaunchRequest, '/api/server_latest_launch_request')


# === /api/server_count_by_region ===


class ServerCountByRegion(run.restful.Resource):
    """
    Returns a summary of the number of servers running in each region.
    """
    def get(self):
        q = run.session.query(run.provider_region.c.name.label('key'), func.count(run.cached_server.c.server_id).label('y'))\
            .outerjoin(run.cached_server, run.provider_region.c.provider_region_id == run.cached_server.c.provider_region_id)\
            .outerjoin(run.cloud, run.cached_server.c.cloud_id == run.cloud.c.cloud_id)\
            .filter(run.cached_server.c.current_state == 'RUNNING')\
            .group_by(run.provider_region.c.name).order_by(desc(func.count(run.cached_server.c.server_id))).all()

        return jsonify(results=q)

run.api.add_resource(ServerCountByRegion, '/api/server_count_by_region')


# === /api/server_count_by_region ===


class ServerCountByCloud(run.restful.Resource):
    """
    Returns a summary of the number of servers running in each cloud.
    """
    def get(self):
        q = run.session.query(run.cloud.c.name.label('label'), func.count(run.server.c.cloud).label('value'))\
            .outerjoin(run.server, run.server.c.cloud == run.cloud.c.cloud_id)\
            .group_by(run.server.c.cloud)\
            .having(func.count(run.server.c.cloud) > 0)\
            .order_by(desc(func.count(run.server.c.cloud))).all()

        return jsonify(results=q)

run.api.add_resource(ServerCountByCloud, '/api/server_count_by_cloud')


# === /api/top_users_server_launch ===


class TopUsers(run.restful.Resource):
    """
    Returns a summarized list of users and the number of servers
    in any state (TERMINATED, RUNNING, etc.) alterable by passing in a state.

    If no count value is passed, will return the top 10 server owners

    Examples:
    /api/top_users_server_launch?limit=5&state=TERMINATED
    /api/top_users_server_launch?state=STOPPED
    """
    def get(self):
        if 'limit' in request.args:
            limit = int(request.args['limit'])
        else:
            limit = 10

        if 'state' in request.args:
            state = request.args['state']
        else:
            state = 'RUNNING'

        q = run.session.query(run.person.c.person_id, func.count(run.cached_server.c.server_id).label('count'),
                              run.person.c.email_address, run.person.c.first_name, run.person.c.last_name)\
            .select_from(run.server)\
            .outerjoin(run.cached_server, run.cached_server.c.server_id == run.server.c.server_id)\
            .outerjoin(run.enstratus_user, run.server.c.owning_user == run.enstratus_user.c.enstratus_user_id)\
            .outerjoin(run.person, run.person.c.person_id == run.enstratus_user.c.person)\
            .filter(run.cached_server.c.current_state == state)\
            .filter(run.person.c.email_address != None)\
            .group_by(run.server.c.owning_user).order_by(desc(func.count(run.cached_server.c.server_id)))\
            .limit(limit).all()

        return jsonify(results=q)

run.api.add_resource(TopUsers, '/api/top_users_server_launch')


# === /api/platform_running_servers ===


class PlatformRunningServers(run.restful.Resource):
    """
    Returns a breakdown of platforms of RUNNING servers.
    """
    def get(self):
        q = run.session.query(run.cached_server.c.platform.label('label'), func.count(run.cached_server.c).label('value'))\
            .filter(run.cached_server.c.current_state == 'RUNNING')\
            .group_by(run.cached_server.c.platform).order_by(desc(func.count(run.cached_server.c).label('count'))).all()

        return jsonify(results=q)

run.api.add_resource(PlatformRunningServers, '/api/platform_running_servers')


# === /api/server_event_location ===


class ServerEventLocation(run.restful.Resource):
    """
    Returns a count of externally (outside of DCM) and internally (created with DCM) created servers.
    """
    def get(self):
        q = run.session.query(func.IF(run.server_change.c.external == 'Y','external','internal').label('location'),\
                              func.count(run.server_change.c).label('count'))\
            .filter(run.server_change.c.event_type == 'CREATE')\
            .group_by(run.server_change.c.external)\
            .all()

        return jsonify(results=q)

run.api.add_resource(ServerEventLocation, '/api/server_event_location')


# === /api/min_max_server_launch ===


class MinMaxServerLaunch(run.restful.Resource):
    """
    Returns the first and last successful server launch date.

    **Returns**:

        {
            results: [
                {
                    first_launch: 1389808402057,
                    last_launch: 1398216186150
                }
            ]
        }
    """
    def get(self):
        q = run.session.query(func.min(run.cached_server.c.created_timestamp).label('first_launch'),
                              func.max(run.cached_server.c.created_timestamp).label('last_launch'))\
            .order_by(desc(run.cached_server.c.server_id)).limit(1).all()
        return jsonify(results=q)

run.api.add_resource(MinMaxServerLaunch, '/api/min_max_server_launch')


# === /api/total_server_create_events ===


class TotalServerCreateEvents(run.restful.Resource):
    """
    Returns the count of server create events.
    """
    def get(self):
        q = run.session.query(func.count(run.server_change.c).label('count'))\
            .filter(run.server_change.c.event_type == 'CREATE').all()

        return jsonify(results=q)

run.api.add_resource(TotalServerCreateEvents, '/api/total_server_create_events')


    #
    # class ServersByBudgetAndState(run.restful.Resource):
    #   '''
    #   Returns a count of servers per budget code
    #   '''
    #   def get(self):
    #     q = run.session.query(run.billing_code.c.name,\
    #         func.sum(func.IF(run.cached_server.c.current_state == 'TERMINATED', 1, 0)).label('TERMINATED'),\
    #         func.sum(func.IF(run.cached_server.c.current_state == 'RUNNING', 1, 0)).label('RUNNING'),\
    #         func.sum(func.IF(run.cached_server.c.current_state == 'STOPPED', 1, 0)).label('STOPPED'))\
    #         .outerjoin(run.server, run.billing_code.c.billing_code_id == run.server.c.budget)\
    #         .outerjoin(run.cached_server, run.server.c.server_id == run.cached_server.c.server_id)\
    #         .group_by(run.server.c.budget)\
    #         .filter(run.cached_server.c.current_state != None)\
    #         .order_by(desc(func.count(run.billing_code.c.billing_code_id).label('count')))\
    #         .all()
    #     run.session.close()
    #     return jsonify(results=q)
    #
    # run.api.add_resource(ServersByBudgetAndState, '/api/servers_by_budget_and_state')
    #
    # class ServersWithAgentAndState(run.restful.Resource):
    #   '''
    #   Returns a count of servers per budget code
    #   '''
    #   def get(self):
    #     q = run.session.query(run.cached_server.c.current_state, run.server_agent.c.version,\
    #         func.count(run.cached_server.c.current_state).label('count'))\
    #         .outerjoin(run.server_agent, run.server_agent.c.server == run.cached_server.c.server_id)\
    #         .filter(run.server_age.c.version != None)\
    #         .group_by(run.server_agent.c.version, run.cached_server.c.current_state)\
    #         .all()
    #     run.session.close()
    #     return jsonify(results=q)
    #
    # run.api.add_resource(ServersWithAgentAndState, '/api/servers_with_agent_and_state')
    #
    # class ServerTimeToRunning(run.restful.Resource):
    #   '''
    #   Returns the time it took for a server launched from within DCM to reach a state of RUNNING.
    #   '''
    #   def get(self, server_id):
    #     q = run.session.query(run.server.c.server_id, run.server_change.c.external, (run.server.c.created_timestamp/1000).label('created_timestamp'), (run.server_change.c.event_timestamp/1000).label('running_timestamp'), func.round(((run.server_change.c.event_timestamp/1000)-(run.server.c.created_timestamp/1000))).label('seconds_to_complete')).outerjoin(run.server_change, run.server.c.server_id == run.server_change.c.server_id).filter(run.server.c.server_id == server_id).filter(run.server_change.c.details.like('%{"currentState":{"new":"RUNNING","old":"PENDING"}%')).all()
    #     run.session.close()
    #     return jsonify(results=q)
    #
    # class ServerLaunchAverage(run.restful.Resource):
    #   '''
    #   Returns the time it took for a server launched from within DCM to reach a state of RUNNING.
    #   '''
    #   def get(self):
    #     q = run.session.query(func.round(func.avg((run.server_change.c.event_timestamp/1000)-(run.server.c.created_timestamp/1000))).label('seconds_to_complete'))\
    #       .select_from(run.server)\
    #       .outerjoin(run.server_change, run.server.c.server_id == run.server_change.c.server_id)\
    #       .filter(run.server_change.c.details.like('%{"currentState":{"new":"RUNNING","old":"PENDING"}%'))\
    #       .limit(100).all()
    #     run.session.close()
    #     return jsonify(results=q)
    #
    # run.api.add_resource(ServerLaunchAverage, '/api/server/launch_average')
    #
    # class ServerLifecycle(run.restful.Resource):
    #   '''
    #   Breakdown of various lifecycle stages of a server launch (Launch, Agent Start, Agent Handshake, CM Start, CM End, Running state).
    #   '''
    #   def get(self, server_id):
    #     agent_start = run.session.query((run.agent_item.c.activity_timestamp/1000).label('agent_start')).filter(run.agent_item.c.server == server_id).filter((run.agent_item.c.message.like('%[ServerListener] [Server Listener - STARTING...]%'))).limit(1).all()
    #
    #     if len(agent_start) > 0 and agent_start[0].agent_start is not None:
    #       agent_start_var = int(agent_start[0].agent_start)
    #     else:
    #       agent_start_var = None
    #
    #     agent_handshake = run.session.query((run.agent_item.c.activity_timestamp/1000).label('agent_handshake')).filter(run.agent_item.c.server == server_id).filter((run.agent_item.c.message.like('%[AgentSecurity] [Agent is now running.]%'))).limit(1).all()
    #
    #     if len(agent_handshake) > 0 and agent_handshake[0].agent_handshake is not None:
    #       agent_handshake_var = int(agent_handshake[0].agent_handshake)
    #     else:
    #       agent_handshake_var = None
    #
    #     cm_start = run.session.query((run.agent_item.c.activity_timestamp/1000).label('cm_start')).filter(run.agent_item.c.server == server_id).filter((run.agent_item.c.message.like('%[ConfigureServerWithChef] [Running chef configuration management]%'))).limit(1).all()
    #
    #     if len(cm_start) > 0 and cm_start[0].cm_start is not None:
    #       cm_start_var = int(cm_start[0].cm_start)
    #     else:
    #       cm_start_var = None
    #
    #     cm_end = run.session.query((run.agent_item.c.activity_timestamp/1000).label('cm_end')).filter(run.agent_item.c.server == server_id).filter((run.agent_item.c.message.like('%[Finished running configuration management%'))).limit(1).all()
    #
    #     if len(cm_end) > 0 and cm_end[0].cm_end is not None:
    #       cm_end_var = int(cm_end[0].cm_end)
    #     else:
    #       cm_end_var = None
    #
    #     q = run.session.query(run.server.c.server_id, run.server_change.c.external,  func.cast(agent_start_var, Integer).label('agent_start'), func.cast(agent_handshake_var, Integer).label('agent_handshake'), func.cast(cm_start_var, Integer).label('cm_start'), func.cast(cm_end_var, Integer).label('cm_end'), func.cast((run.server.c.created_timestamp/1000), Integer).label('created_timestamp'), func.cast((run.server_change.c.event_timestamp/1000), Integer).label('running_timestamp'), func.round(((run.server_change.c.event_timestamp/1000)-(run.server.c.created_timestamp/1000))).label('seconds_to_complete')).outerjoin(run.server_change, run.server.c.server_id == run.server_change.c.server_id).filter(run.server.c.server_id == server_id).filter(run.server_change.c.details.like('%{"currentState":{"new":"RUNNING","old":"PENDING"}%')).all()
    #
    #     return jsonify(results=q)
    #
    # run.api.add_resource(ServerLifecycle, '/api/server_lifecycle/<int:server_id>')
