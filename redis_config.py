from redis import asyncio as aioredis

REDIS_CONFIG = {
    'host': 'localhost',
    'port': 6379,
    'db': 0,
    'decode_responses': True
}

async def get_redis_pool():
    return await aioredis.from_url(
        f"redis://{REDIS_CONFIG['host']}:{REDIS_CONFIG['port']}", 
        db=REDIS_CONFIG['db'],
        decode_responses=REDIS_CONFIG['decode_responses']
    )