"""Simple time‑to‑live cache for retrieval results."""

import time
from typing import Any, Dict


class TTLCache:
    """A very small in‑memory cache with an expiration time."""

    def __init__(self, ttl_sec: int = 60):
        self.ttl = ttl_sec
        self.data: Dict[str, Dict[str, Any]] = {}

    def get(self, key: str) -> Any | None:
        val = self.data.get(key)
        if not val:
            return None
        if time.time() - val["ts"] > self.ttl:
            self.data.pop(key, None)
            return None
        return val["value"]

    def set(self, key: str, value: Any) -> None:
        self.data[key] = {"value": value, "ts": time.time()}


# Global retrieval cache instance
retrieval_cache = TTLCache(90)