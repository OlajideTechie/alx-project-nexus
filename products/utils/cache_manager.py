from django.core.cache import cache

import logging

logger = logging.getLogger(__name__)
logger.info("Cache HIT for key xyz")

class CacheManager:
    def __init__(self, prefix, timeout=300):
        """
        prefix: str - cache key prefix for namespace separation (e.g., 'products', 'categories')
        timeout: int - cache TTL in seconds
        """
        self.prefix = prefix
        self.timeout = timeout

    def get_cache_key(self, identifier):
        """
        Returns a fully qualified cache key based on prefix and identifier (e.g., page number, user role)
        """
        return f"{self.prefix}_{identifier}"

    def get(self, identifier):
        key = self.get_cache_key(identifier)
        data = cache.get(key)
        if data:
            logger.info(f"Cache HIT: {key}")
        else:
            logger.info(f"Cache MISS: {key}")
        return data

    def set(self, identifier, data):
        key = self.get_cache_key(identifier)
        cache.set(key, data, timeout=self.timeout)
        logger.info(f"Cache SET: {key} for {self.timeout} seconds")

    def invalidate(self):
        """
        Deletes all keys with the current prefix.
        """
        pattern = f"{self.prefix}_*"
        try:
            cache.delete_pattern(pattern)
            logger.info(f"Cache INVALIDATED for pattern: {pattern}")
        except NotImplementedError:
            logger.warning("Cache backend does not support delete_pattern. Manual invalidation needed.")
