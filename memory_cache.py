import json
import os
import asyncio

from typing import Hashable
from pathlib import Path
from datetime import datetime, timedelta

BASE_DIR = Path(__file__).resolve().parent


class MemoryCache:

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(MemoryCache, cls).__new__(cls)
        return cls.instance
    
    def __init__(self) -> None:
        if os.path.exists(BASE_DIR / 'data_file.json'):
            with open(BASE_DIR / 'data_file.json', 'r') as data_file:
                self._cache = json.load(data_file)         
        else:
            self._cache = dict()
        
        self._ttl_data = dict()
    
    async def get(self, key: Hashable) -> str:
        if len(key) == 0:
            return "ERR wrong number of arguments for 'get' command"
        
        return self._cache.get(key)
    
    async def set(self, key: Hashable, value: str, ex: int = None) -> str:
        if len(key) == 0 or len(value) == 0:
            return "ERR wrong number of arguments for 'set' command"
        
        self._cache[key] = value

        if None != ex:
            self._ttl_data[key] = ex
            loop = asyncio.get_event_loop()
            loop.run_in_executor(None, self._time_to_live, key, ex)

        return 'OK'
    
    async def delete(self, key: Hashable) -> int:
        try:
            del self._cache[key]
            return 1

        except KeyError:
            return 0

    async def ttl(self, key: str) -> int:
        try:
            return self._ttl_data[key]
        except KeyError:
            return -2

    async def save(self) -> str:
        with open(BASE_DIR / 'data_file.json', 'w') as data_file:
            json.dump(self._cache, data_file, indent=4)
        
        return 'OK'
    
    def _time_to_live(self, key: Hashable, ex: int) -> None:
        time_of_delete = datetime.now() + timedelta(seconds=ex)

        while True:
            if time_of_delete.second > datetime.now().second:
                seconds = time_of_delete.second - datetime.now().second
                if self._ttl_data[key] != seconds:
                    self._ttl_data[key] = seconds
            else:
                del self._cache[key]
                del self._ttl_data[key]
                break