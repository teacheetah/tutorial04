from aiohttp import web

from .views import index, login
from .api.routes import setup_routes as api_setup_routes

def setup_routes(app: web.Application) -> None:
    app.add_routes([web.get('/', index)])
    app.add_routes([web.get('/login', login)])

    api_setup_routes(app)