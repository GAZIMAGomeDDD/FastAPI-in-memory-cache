import json
import os
import asyncio
import time

from typing import Hashable, Optional
from pathlib import Path
from collections import OrderedDict

BASE_DIR = Path(__file__).resolve().parent
TTL = Optional[int]


class MemoryCache:

    _cache: OrderedDict
    _ttl_data: OrderedDict

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls._instance = super(MemoryCache, cls).__new__(cls)
        
        return cls._instance
    
    def __init__(self) -> None:
        if os.path.exists(BASE_DIR / 'data_file.json'):
            with open(BASE_DIR / 'data_file.json', 'r') as data_file:
                self._cache = OrderedDict(json.load(data_file))         
        else:
            self._cache = OrderedDict()
        
        self._ttl_data = OrderedDict()
    
    async def get(self, key: Hashable) -> str:
        if len(key) == 0:
            return "ERR wrong number of arguments for 'get' command"
        
        return self._cache.get(key)
    
    async def set(self, key: Hashable, value: str, ex: TTL) -> str:
        if len(key) == 0 or len(value) == 0:
            return "ERR wrong number of arguments for 'set' command"
        
        self._cache[key] = value

        if None != ex:
            self._ttl_data[key] = ex
            loop = asyncio.get_event_loop()
            loop.run_in_executor(None, self._expire_times, key, ex)

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
        with open(BASE_DIR / 'data_file.json', 'w') as data_file:
            json.dump(self._cache, data_file, indent=4)
        
        return 'OK'
    
    def _expire_times(self, key: Hashable, ex: TTL) -> None:
        time_of_delete = time.time() + ex

        while time_of_delete > time.time():
            seconds = round(time_of_delete - time.time())
            self._ttl_data[key] = seconds

        del self._cache[key]
        del self._ttl_data[key]
