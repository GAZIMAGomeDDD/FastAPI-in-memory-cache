from pydantic import BaseModel
from typing import List, Optional


class GET(BaseModel):

    key: str


class SET(BaseModel):

    key: str
    value: str
    ttl: Optional[int] = None


class TTL(BaseModel):
    
    key: str

class DEL(BaseModel):
    
    keys: List[str]


class KEYS(BaseModel):

    pattern: str


class HSETList(BaseModel):

    key: str
    value: str


class HSET(BaseModel):
    
    key: str
    fields: List[HSETList]


class HGET(BaseModel):

    key: str
    field: str


class RLPUSH(BaseModel):
    key: str
    elements: List[str]


class LSET(BaseModel):
    key: str
    index: int
    element: str


class LGET(BaseModel):
    key: str
    index: int
