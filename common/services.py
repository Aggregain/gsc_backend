
from django.core.cache import cache

class Cacher:

    def __init__(self, cache_key, ttl=3600):
        self.cache_key = cache_key
        self.ttl = ttl

    def set_value(self, value):
        cache.set(self.cache_key, value, self.ttl)


    def remove_value(self):
        cache.delete(self.cache_key)

    def get_value(self):
        return cache.get(self.cache_key)

    @staticmethod
    def clear_cache():
        cache.clear()