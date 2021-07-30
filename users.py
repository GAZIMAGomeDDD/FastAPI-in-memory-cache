import asyncio
import os
import pickle

from memory_cache import BASE_DIR
from string import ascii_uppercase, ascii_lowercase, digits
from random import sample
from passlib.handlers.sha2_crypt import sha256_crypt


class UsersData:

    def __init__(self) -> None:
        if os.path.exists(BASE_DIR / 'users'):
            with open(BASE_DIR / 'users', 'rb') as dump:
                self._users_data = pickle.load(dump)
        else:     
            self._users_data = dict()

        self._tokens = dict()

    async def register(self, login: str, password: str) -> str:
        if self._users_data.get(login):
            return 'Login already exists'
        
        self._users_data[login] = self._get_password_hash(password)
        asyncio.get_event_loop().run_in_executor(
            executor=None, 
            func=self._save
        )
        return 'OK'            
        
    async def auth(self, login: str, password: str) -> str:
        try:
            hashed_password = self._users_data[login]
        except KeyError:
            return 'Login not found'
        
        if self._verify_password(password, hashed_password):
            token = self._create_token()
            self._tokens[token] = True
            return token
        
        return 'Password mismatch'
    
    def check_token(self, token: str) -> bool:
        try:
            self._tokens[token]
            return True
        except KeyError:
            return False

    @staticmethod
    def _create_token() -> str:
        return ''.join(sample(ascii_uppercase + ascii_lowercase + digits, 10))

    @staticmethod
    def _verify_password(password: str, hashed_password: str) -> bool:
        return sha256_crypt.verify(password, hashed_password)

    @staticmethod
    def _get_password_hash(password: str) -> sha256_crypt.hash:
        return sha256_crypt.hash(password)
    
    def _save(self) -> None:
        with open(BASE_DIR / 'users', 'wb') as dump:
            pickle.dump(self._users_data, dump)
