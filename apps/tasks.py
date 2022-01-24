import aioredis


async def setup_redis(app):
    pool = await aioredis.create_redis_pool((
        app['config']['redis']['HOST'],
        app['config']['redis']['PORT']), 
        db=app['config']['redis']['DB'],
        minsize=5, 
        maxsize=10
    )

    async def close_redis(app):
        pool.close()
        await pool.wait_closed()

    app.on_cleanup.append(close_redis)
    app['redis_pool'] = pool
    return pool
