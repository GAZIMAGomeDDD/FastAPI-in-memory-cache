from pydantic import BaseModel
from typing import Optional


class GET(BaseModel):

    key: str


class SET(GET):

    key: str
    value: str
    ex: Optional[int] = None


class TTL(GET):
    pass


class DEL(GET):
    pass
