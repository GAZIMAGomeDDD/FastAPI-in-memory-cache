import os
import asyncio
import time
import pickle

from concurrent.futures import ThreadPoolExecutor
from re import search
from typing import Dict, Optional, List, Union
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
TTL = Optional[int]


class MemoryCache:
    
    def __init__(self) -> None:
        if os.path.exists(BASE_DIR / 'dump'):
            with open(BASE_DIR / 'dump', 'rb') as dump:
                self._cache = pickle.load(dump)
        else:
            self._cache = dict()
        
        self._ttl_data = dict()
        self._hash_data = dict()
        self._io_pool_exc = ThreadPoolExecutor()
        self._loop = asyncio.get_event_loop()
    
    async def get(self, key: str) -> str:
        if self._hash_data.get(key):
            return 'WRONGTYPE Operation against a key holding the wrong kind of value'
        
        return self._cache.get(key)
    
    async def set(self, key: str, value: str, ttl: TTL) -> str:
        if self._hash_data.get(key):
            del self._hash_data[key]

        if self._ttl_data.get(key) != None:
            self._ttl_data[key]['ttl_stop'] = True
        
        if ttl != None:
            if ttl < 1:
                return 'ERR invalid expire time in set'

            self._cache[key] = value
            self._ttl_data[key] = dict(ttl=ttl, ttl_stop=False)
            self._loop.run_in_executor(self._io_pool_exc, self._expire_times, key, ttl)
        else:
            self._cache[key] = value

        return 'OK'
    
    async def delete(self, keys: List[str]) -> int:
        count = 0
 
        for key in keys:
            if self._cache.get(key):
                count += 1

            if self._ttl_data.get(key) != None:
                self._ttl_data[key]['ttl_stop'] = True

            try:
                del self._cache[key]
                del self._hash_data[key]
            except KeyError:
                pass
                
        return count

    async def ttl(self, key: str) -> int:
        try:
            return self._ttl_data[key]['ttl']
        
        except KeyError:
            return -2

    async def save(self) -> str:
        self._loop.run_in_executor(
            executor=self._io_pool_exc, 
            func=self._save
        )
        
        return 'OK'

    async def keys(self, pattern: str) -> List[str]:
        
        return [key for key in self._cache.keys() if search(pattern, key) != None]
       
    async def hset(self, key: str, fields: List[Dict]) -> Union[str, int]:
        count = 0

        if not self._hash_data.get(key, False):
            if self._cache.get(key):
                return 'WRONGTYPE Operation against a key holding the wrong kind of value'

            self._cache[key] = dict()
            self._hash_data[key] = True

        for field in fields:
            if not self._cache[key].get(field['key']):
                count += 1
            
            self._cache[key].update({field['key']: field['key']})
                
        return count

    async def hget(self, key: str, field: str) -> Optional[str]:
        if not self._hash_data.get(key, False):
            if not self._cache.get(key, False):
                return None

            return 'WRONGTYPE Operation against a key holding the wrong kind of value'
        
        return self._cache[key][field]


    def _expire_times(self, key: str, ttl: TTL) -> None:
        timer = time.time() + ttl

        while timer > time.time():

            if self._ttl_data[key]['ttl_stop']:
                del self._cache[key]
                del self._ttl_data[key]

                break

            time.sleep(1)
            seconds = round(timer - time.time())
            self._ttl_data[key]['ttl'] = seconds

        if self._ttl_data.get(key):
            del self._cache[key]
            del self._ttl_data[key]

    def _save(self) -> None:
        with open(BASE_DIR / 'dump', 'wb') as dump:
            pickle.dump(self._cache, dump)
