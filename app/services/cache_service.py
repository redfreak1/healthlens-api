import json
from typing import Optional, Any

# Try to import redis, fallback gracefully if not available
try:
    import redis.asyncio as redis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False
    print("⚠️  Redis not available - using in-memory cache fallback")

# Try to import settings, fallback gracefully
try:
    from app.config import settings
except ImportError:
    print("⚠️  Settings not available - using defaults")
    class MockSettings:
        redis_url = "redis://localhost:6379"
    settings = MockSettings()

class CacheService:
    def __init__(self):
        self.redis_client = None
        self.memory_cache = {}  # Fallback in-memory cache
    
    async def _get_client(self):
        if not self.redis_client:
            if REDIS_AVAILABLE:
                try:
                    self.redis_client = redis.from_url(settings.redis_url)
                    # Test the connection
                    await self.redis_client.ping()
                    print("✅ Redis connection established")
                except Exception as e:
                    print(f"⚠️  Redis connection failed: {e}")
                    print("📝 Using in-memory cache fallback")
                    self.redis_client = None
            else:
                print("📝 Using in-memory cache (Redis not available)")
                self.redis_client = None
        return self.redis_client
    
    async def get(self, key: str) -> Optional[dict]:
        """Get cached value by key"""
        try:
            client = await self._get_client()
            if isinstance(client, dict):
                # In-memory fallback
                return client.get(key)
            
            value = await client.get(key)
            if value:
                return json.loads(value)
            return None
        except Exception as e:
            print(f"Cache get error: {e}")
            return None
    
    async def set(self, key: str, value: dict, ttl: int = 3600) -> bool:
        """Set cache value with TTL in seconds"""
        try:
            client = await self._get_client()
            if isinstance(client, dict):
                # In-memory fallback
                client[key] = value
                return True
            
            await client.setex(key, ttl, json.dumps(value))
            return True
        except Exception as e:
            print(f"Cache set error: {e}")
            return False
    
    async def delete(self, key: str) -> bool:
        """Delete cache entry"""
        try:
            client = await self._get_client()
            if isinstance(client, dict):
                client.pop(key, None)
                return True
            
            await client.delete(key)
            return True
        except Exception as e:
            print(f"Cache delete error: {e}")
            return False
    
    async def clear_pattern(self, pattern: str) -> bool:
        """Clear all keys matching pattern"""
        try:
            client = await self._get_client()
            if isinstance(client, dict):
                keys_to_delete = [k for k in client.keys() if pattern in k]
                for k in keys_to_delete:
                    del client[k]
                return True
            
            keys = await client.keys(pattern)
            if keys:
                await client.delete(*keys)
            return True
        except Exception as e:
            print(f"Cache clear pattern error: {e}")
            return False