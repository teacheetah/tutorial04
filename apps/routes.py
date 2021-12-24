from aiohttp import web

from .auth.routes import setup_routes as auth_setup_routes


def setup_routes(app: web.Application) -> None:
    auth_setup_routes(app)
