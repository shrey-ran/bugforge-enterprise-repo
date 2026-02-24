"""Caching layer configuration and utilities."""
import time

class SimpleCache:
    def __init__(self, default_ttl: int = 300):
        self._store = {}
        self.default_ttl = default_ttl
        self.hits = 0
        self.misses = 0
    
    def get(self, key: str):
        if key in self._store:
            value, expiry = self._store[key]
            if time.time() < expiry:
                self.hits += 1
                return value
            else:
                del self._store[key]
        self.misses += 1
        return None
    
    def set(self, key: str, value, ttl: int = None):
        expiry = time.time() + (ttl or self.default_ttl)
        self._store[key] = (value, expiry)
    
    def delete(self, key: str) -> bool:
        if key in self._store:
            del self._store[key]
            return True
        return False
    
    def clear(self):
        self._store.clear()
        self.hits = 0
        self.misses = 0
    
    def get_stats(self) -> dict:
        total = self.hits + self.misses
        hit_rate = (self.hits / total * 100) if total > 0 else 0
        return {
            "hits": self.hits,
            "misses": self.misses,
            "hit_rate": f"{hit_rate:.1f}%",
            "stored_keys": len(self._store)
        }
