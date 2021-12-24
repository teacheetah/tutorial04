#!/usr/bin/env python
import os
import jinja2
import asyncio
import logging
import logging.config
import aiohttp_jinja2
from aiohttp import web
from pathlib import Path
from typing import List

from settings import LOGGING, DATABASE
from apps.routes import setup_routes
from apps.db import setup_db

async def init_app() -> web.Application:
    # set logging config
    logging.config.dictConfig(LOGGING)

    # build web app
    app = web.Application()

    # add app configs
    app['config'] = {}
    app['config']['database'] = DATABASE

    # add routes
    setup_routes(app)

    # setup db connections
    await setup_db(app)

    # html templates
    path = Path(__file__).parent
    aiohttp_jinja2.setup(app,
        loader=jinja2.FileSystemLoader(str(path / 'apps/auth/templates'))
    )

    return app

def main(argv: List[str]) -> None:
    loop = asyncio.get_event_loop()
    app = loop.run_until_complete(init_app())

    web.run_app(app,
                host=os.getenv('APP_HOST', 'localhost'),
                port=os.getenv('APP_PORT', '8000'))

if __name__ == '__main__':
    main(sys.argv[1:])
