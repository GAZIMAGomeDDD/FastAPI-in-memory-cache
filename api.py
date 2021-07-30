from schemas import GET, HGET, SET, DEL, TTL, KEYS, HSET
from fastapi import FastAPI, Response
from memory_cache import MemoryCache

app = FastAPI()
cache = MemoryCache()


@app.post("/GET")
async def get(GET: GET) -> Response:
    return await cache.get(
        GET.dict().get('key')
    )


@app.post("/SET")
async def set(SET: SET) -> Response:
    return await cache.set(
        key=SET.dict().get('key'), 
        value=SET.dict().get('value'),
        ttl=SET.dict().get('ttl')
    )


@app.post("/DEL")
async def delete(DEL: DEL) -> Response:
    return await cache.delete(
        keys=DEL.dict().get('keys')
    )


@app.post('/SAVE')
async def save() -> Response:
    return await cache.save()


@app.post('/TTL')
async def ttl(TTL: TTL) -> Response:
    return await cache.ttl(
        key=TTL.dict().get('key')
    )


@app.post('/KEYS')
async def keys(KEYS: KEYS) -> Response:
    return await cache.keys(
        pattern=KEYS.dict().get('pattern')
    )


@app.post('/HSET')
async def hset(HSET: HSET) -> Response:
    return await cache.hset(
        key=HSET.dict().get('key'),
        fields=HSET.dict().get('fields')
    )


@app.post('/HGET')
async def hget(HGET: HGET) -> Response:
    return await cache.hget(
        key=HGET.dict().get('key'),
        field=HGET.dict().get('field')
    )
