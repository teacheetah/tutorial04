import logging
from aiohttp import web

from ..models import AuthDbHelper

logger = logging.getLogger(__name__)


async def health(request):
    db_pool = request.app['db_pool']
    dbhelper = AuthDbHelper(db_pool)
    res = await dbhelper.health()
    if res[0] == 0:
        return web.json_response({'status': 'healthy'})
    return web.json_response({'status': 'unhealthy'}, 
                             status=web.HTTPServiceUnavailable.status_code)

async def api_login(request: web.Request) -> web.Response:
    return web.json_response({'reason': 'Failed to authenticate user'}, 
                             status=web.HTTPUnauthorized.status_code)

async def signup(request: web.Request) -> web.Response:
    if request.content_type != 'application/json':
        return web.json_response({'reason': 'Invalid Content-Type header. '
                                            'Only application/json is allowed'},
                                 status=web.HTTPBadRequest.status_code)

    data = await request.json()

    db_pool = request.app['db_pool']
    try:
        dbhelper = AuthDbHelper(db_pool)
        res = await dbhelper.insert(data)
    except Exception as e:
        return web.json_response({'reason': '%s' % e},
                                 status=web.HTTPBadRequest.status_code)
    else:
        return web.json_response(res)

async def get(request: web.Request) -> web.Response:
    username = request.match_info.get('username', None)
    db_pool = request.app['db_pool']
    try:
        dbhelper = AuthDbHelper(db_pool)
        res = await dbhelper.get(username)
    except Exception as e:
        return web.json_response({'reason': '%s' % e},
                                 status=web.HTTPNotFound.status_code)
    else:
        return web.json_response(res)
