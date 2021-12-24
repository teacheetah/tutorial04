from aiohttp import web

from .views import api_login, signup, get, health


def setup_routes(app: web.Application) -> None:
    app.add_routes(
        [web.post('/api/v1/login', api_login),
         web.post('/api/v1/signup', signup),
         web.get('/api/v1/users/{username}', get),
         web.get('/api/v1/health', health),
        ]
    )
