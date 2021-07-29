from pydantic import BaseModel
from typing import Optional


class GET(BaseModel):

    key: str


class SET(GET):

    value: str
    ex: Optional[int] = None


class TTL(GET):
    pass


class DEL(GET):
    pass


class KEYS(BaseModel):

    pattern: str
