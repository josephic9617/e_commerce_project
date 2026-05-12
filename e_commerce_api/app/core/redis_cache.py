import redis
import json
from app.core.config import settings

redis_client = redis.Redis.from_url(settings.REDIS_URL, decode_responses=True)

def get_cache(key: str):
    try:
        data = redis_client.get(key)
        if data:
            return json.loads(data)
    except Exception as e:
        print(f"Redis get error: {e}")
    return None

def set_cache(key: str, data: dict, expire: int = 3600):
    try:
        redis_client.setex(key, expire, json.dumps(data))
    except Exception as e:
        print(f"Redis set error: {e}")

def delete_cache(key: str):
    try:
        redis_client.delete(key)
    except Exception as e:
        print(f"Redis delete error: {e}")

def clear_cache_pattern(pattern: str):
    try:
        keys = redis_client.keys(pattern)
        if keys:
            redis_client.delete(*keys)
    except Exception as e:
        print(f"Redis clear pattern error: {e}")
