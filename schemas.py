from pydantic import BaseModel
from typing import List, Optional


class GET(BaseModel):

    key: str
    token: str


class SET(BaseModel):

    key: str
    value: str
    ttl: Optional[int] = None
    token: str


class TTL(BaseModel):
    
    key: str
    token: str

class DEL(BaseModel):
    
    keys: List[str]
    token: str


class KEYS(BaseModel):

    pattern: str
    token: str


class HSETList(BaseModel):

    key: str
    value: str


class HSET(BaseModel):
    
    key: str
    fields: List[HSETList]
    token: str


class HGET(BaseModel):

    key: str
    field: str
    token: str


class RLPUSH(BaseModel):
    key: str
    elements: List[str]
    token: str


class LSET(BaseModel):
    key: str
    index: int
    element: str
    token: str


class LGET(BaseModel):
    key: str
    index: int
    token: str


class Register(BaseModel):
    login: str 
    password: str


class Auth(BaseModel):
    login: str 
    password: str


class SAVE(BaseModel):
    token: str
