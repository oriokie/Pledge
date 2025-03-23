import redis
from app.core.config import settings
import json
from typing import Any, Optional

class RedisService:
    def __init__(self):
        self.redis_client = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            decode_responses=True
        )
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from Redis"""
        value = self.redis_client.get(key)
        return json.loads(value) if value else None
    
    def set(self, key: str, value: Any, expire: int = 3600) -> bool:
        """Set value in Redis with expiration time in seconds"""
        return self.redis_client.set(
            key,
            json.dumps(value),
            ex=expire
        )
    
    def delete(self, key: str) -> bool:
        """Delete key from Redis"""
        return bool(self.redis_client.delete(key))
    
    def exists(self, key: str) -> bool:
        """Check if key exists in Redis"""
        return bool(self.redis_client.exists(key))
    
    def clear_cache(self, pattern: str = "*") -> None:
        """Clear all keys matching the pattern"""
        keys = self.redis_client.keys(pattern)
        if keys:
            self.redis_client.delete(*keys)

redis_service = RedisService() 