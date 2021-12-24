import logging
import aiohttp_jinja2
from aiohttp import web


logger = logging.getLogger(__name__)

async def index(request: web.Request) -> web.Response:
    """Load index page"""
    logger.info('Loading index page')
    return aiohttp_jinja2.render_template('index.html', request, {})

async def login(request: web.Request) -> web.Response:
    """Load login page"""
    return aiohttp_jinja2.render_template('login.html', request, {})
