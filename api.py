from schemas import GET, SET, DEL, TTL
from fastapi import FastAPI, Response
from memory_cache import MemoryCache

app = FastAPI()
cache = MemoryCache()


@app.post("/GET")
async def get(GET: GET) -> Response:
    return await cache.get(GET.dict().get('key'))


@app.post("/SET")
async def set(SET: SET) -> Response:
    return await cache.set(
        key=SET.dict().get('key'), 
        value=SET.dict().get('value'),
        ex=SET.dict().get('ex')
    )


@app.post("/DEL")
async def delete(DEL: DEL) -> Response:
    return await cache.delete(
        key=DEL.dict().get('key')
    )

@app.post('/SAVE')
async def save() -> Response:
    return await cache.save()


@app.post('/TTL')
async def ttl(TTL: TTL) -> Response:
    return await cache.ttl(
        key=TTL.dict().get('key')
    )
