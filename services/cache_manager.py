"""
Cache Manager - For Scalability
Caches optimization results to avoid re-processing.
"""

from typing import Optional, Dict
import hashlib
import json
import time

# Simple in-memory cache (for demo)
# In production, use Redis
class SimpleCache:
    """
    Simple cache implementation.
    For production, replace with Redis.
    """
    
    def __init__(self, ttl: int = 604800):  # 7 days default
        self.cache = {}
        self.ttl = ttl
    
    def _generate_key(self, candidate_id: int, job_id: int, job_version: str = None) -> str:
        """Generate cache key."""
        key_data = f"{candidate_id}:{job_id}"
        if job_version:
            key_data += f":{job_version}"
        return hashlib.md5(key_data.encode()).hexdigest()
    
    def get(self, candidate_id: int, job_id: int, job_version: str = None) -> Optional[Dict]:
        """Get cached optimization result."""
        key = self._generate_key(candidate_id, job_id, job_version)
        
        if key in self.cache:
            entry = self.cache[key]
            # Check if expired
            if time.time() - entry['timestamp'] < self.ttl:
                return entry['data']
            else:
                # Expired, remove it
                del self.cache[key]
        
        return None
    
    def set(self, candidate_id: int, job_id: int, data: Dict, job_version: str = None):
        """Cache optimization result."""
        key = self._generate_key(candidate_id, job_id, job_version)
        self.cache[key] = {
            'data': data,
            'timestamp': time.time()
        }
    
    def invalidate(self, candidate_id: int, job_id: int):
        """Invalidate cache for candidate+job."""
        # Simple: clear all (in production, use specific key)
        keys_to_remove = [
            k for k in self.cache.keys()
            if str(candidate_id) in str(k) and str(job_id) in str(k)
        ]
        for k in keys_to_remove:
            del self.cache[k]
    
    def clear(self):
        """Clear all cache."""
        self.cache.clear()
    
    def stats(self) -> Dict:
        """Get cache statistics."""
        total = len(self.cache)
        expired = sum(
            1 for entry in self.cache.values()
            if time.time() - entry['timestamp'] >= self.ttl
        )
        return {
            'total_entries': total,
            'expired_entries': expired,
            'active_entries': total - expired
        }


# Production-ready: Redis implementation
import redis
import json
import os

class RedisCache:
    """Production Redis cache implementation."""
    
    def __init__(self, ttl: int = 604800):
        """Initialize Redis cache.
        
        Args:
            ttl: Time to live in seconds (default: 7 days)
        """
        redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379/1')
        try:
            self.redis_client = redis.from_url(
                redis_url,
                decode_responses=True,
                socket_connect_timeout=5,
                socket_timeout=5
            )
            # Test connection
            self.redis_client.ping()
            self.ttl = ttl
            self._redis_available = True
        except Exception as e:
            print(f"⚠️  Redis not available, using in-memory cache: {e}")
            self._redis_available = False
            self._fallback_cache = SimpleCache(ttl=ttl)
    
    def _generate_key(self, candidate_id: int, job_id: int, job_version: str = None) -> str:
        """Generate cache key."""
        key_data = f"opt:{candidate_id}:{job_id}"
        if job_version:
            key_data += f":{job_version}"
        return key_data
    
    def get(self, candidate_id: int, job_id: int, job_version: str = None) -> Optional[Dict]:
        """Get cached optimization result."""
        if not self._redis_available:
            return self._fallback_cache.get(candidate_id, job_id, job_version)
        
        try:
            key = self._generate_key(candidate_id, job_id, job_version)
            data = self.redis_client.get(key)
            if data:
                return json.loads(data)
            return None
        except Exception as e:
            print(f"Redis get error: {e}")
            return None
    
    def set(self, candidate_id: int, job_id: int, data: Dict, job_version: str = None):
        """Cache optimization result."""
        if not self._redis_available:
            self._fallback_cache.set(candidate_id, job_id, data, job_version)
            return
        
        try:
            key = self._generate_key(candidate_id, job_id, job_version)
            self.redis_client.setex(
                key,
                self.ttl,
                json.dumps(data)
            )
        except Exception as e:
            print(f"Redis set error: {e}")
    
    def invalidate(self, candidate_id: int, job_id: int):
        """Invalidate cache for candidate+job."""
        if not self._redis_available:
            self._fallback_cache.invalidate(candidate_id, job_id)
            return
        
        try:
            pattern = f"opt:{candidate_id}:{job_id}*"
            keys = self.redis_client.keys(pattern)
            if keys:
                self.redis_client.delete(*keys)
        except Exception as e:
            print(f"Redis invalidate error: {e}")
    
    def clear(self):
        """Clear all cache."""
        if not self._redis_available:
            self._fallback_cache.clear()
            return
        
        try:
            pattern = "opt:*"
            keys = self.redis_client.keys(pattern)
            if keys:
                self.redis_client.delete(*keys)
        except Exception as e:
            print(f"Redis clear error: {e}")
    
    def stats(self) -> Dict:
        """Get cache statistics."""
        if not self._redis_available:
            return self._fallback_cache.stats()
        
        try:
            pattern = "opt:*"
            keys = self.redis_client.keys(pattern)
            total = len(keys) if keys else 0
            
            return {
                'total_entries': total,
                'expired_entries': 0,  # Redis handles TTL automatically
                'active_entries': total,
                'backend': 'redis'
            }
        except Exception as e:
            return {
                'total_entries': 0,
                'expired_entries': 0,
                'active_entries': 0,
                'backend': 'error',
                'error': str(e)
            }


# Global cache instance - tries Redis first, falls back to in-memory
try:
    optimization_cache = RedisCache()
except Exception:
    optimization_cache = SimpleCache()

