from __future__ import annotations

from typing import Dict, Generic, Optional, TypeVar

T = TypeVar("T")


class CacheManager(Generic[T]):
    def __init__(self) -> None:
        self._cache: Dict[str, T] = {}

    def get(self, key: str) -> Optional[T]:
        return self._cache.get(key)

    def set(self, key: str, value: T) -> None:
        self._cache[key] = value

    def invalidate(self, key: str) -> None:
        self._cache.pop(key, None)

    def clear(self) -> None:
        self._cache.clear()
