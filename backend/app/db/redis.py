from redis import Redis
from ..core.config import settings

redis_client = Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    decode_responses=True
)

def get_redis():
    try:
        yield redis_client
    finally:
        redis_client.close() 