import os
import asyncio
import time
import pickle

from concurrent.futures import ThreadPoolExecutor
from re import search
from typing import Hashable, Optional, List
from pathlib import Path
from collections import OrderedDict

BASE_DIR = Path(__file__).resolve().parent
TTL = Optional[int]


class MemoryCache:

    _cache: OrderedDict
    _ttl_data: OrderedDict
    
    def __init__(self) -> None:
        if os.path.exists(BASE_DIR / 'dump'):
            with open(BASE_DIR / 'dump', 'rb') as dump:
                self._cache = OrderedDict(pickle.load(dump))
        else:
            self._cache = OrderedDict()
        
        self._ttl_data = OrderedDict()
        self._io_pool_exc = ThreadPoolExecutor()
        self._loop = asyncio.get_event_loop()
    
    async def get(self, key: Hashable) -> str:
        if len(key) == 0:
            return "ERR wrong number of arguments for 'get' command"
        
        return self._cache.get(key)
    
    async def set(self, key: Hashable, value: str, ex: TTL) -> str:
        if len(key) == 0 or len(value) == 0:
            return "ERR wrong number of arguments for 'set' command"
        
        self._cache[key] = value

        if None != ex:
            if ex < 1:
                return "ERR wrong number of arguments for 'set' command"

            self._ttl_data[key] = ex
            self._loop.run_in_executor(self._io_pool_exc, self._expire_times, key, ex)

        return 'OK'
    
    async def delete(self, key: Hashable) -> int:
        try:
            del self._cache[key]
            return 1

        except KeyError:
            return 0

    async def ttl(self, key: Hashable) -> int:
        try:
            return self._ttl_data[key]
        
        except KeyError:
            return -2

    async def save(self) -> str:
        self._loop.run_in_executor(self._io_pool_exc, self._save)
        
        return 'OK'

    async def keys(self, pattern: str) -> List[Hashable]:
        return [key for key in self._cache.keys() if search(pattern, key) != None]
    
    def _expire_times(self, key: Hashable, ex: TTL) -> None:
        timer = time.time() + ex

        while timer > time.time():
            time.sleep(1)
            seconds = round(timer - time.time())
            self._ttl_data[key] = seconds

        del self._cache[key]
        del self._ttl_data[key]

    def _save(self) -> None:
        with open(BASE_DIR / 'dump', 'wb') as dump:
            pickle.dump(self._cache, dump)
