import logging
import aiopg.sa
from sqlalchemy import create_engine

from apps.auth.models import metadata

logger = logging.getLogger(__name__)


async def close_pg(app):
    logger.info('Closing pgsql connections...')

    app['db_pool'].close()
    await app['db_pool'].wait_closed()

async def init_pg(app):
    config = app['config']['database']
    engine = await aiopg.sa.create_engine(
        database=config['NAME'],
        user=config['USER'],
        password=config['PASSWORD'],
        host=config['HOST'],
        port=config['PORT'],
        minsize=config['MINSIZE'],
        maxsize=config['MAXSIZE'],
    )
    app['db_pool'] = engine

    app.on_cleanup.append(close_pg)

    return engine

def construct_db_url(config):
    DSN = "postgresql://{user}:{password}@{host}:{port}/{database}"
    return DSN.format(
        user=config['USER'],
        password=config['PASSWORD'],
        host=config['HOST'],
        port=config['PORT'],
        database=config['NAME'],
    )

def create_tables(app):
    """ Create tables 
    This is a synchronous task, regardless of async aiohttp
    """
    logger.info('Creating database tables...')

    config = app['config']['database']
    url = construct_db_url(config)
    engine = create_engine(url)
    metadata.create_all(engine, checkfirst=True)

    logger.info('Database tables are created...')

async def setup_db(app):
    logger.info('Initializing pgsql connections...')

    await init_pg(app)

    create_tables(app)

    logger.info('Pgsql connections are created...')