from users import UsersData
from schemas import (Auth, GET, HGET, LGET, 
                    LSET, RLPUSH, Register, SAVE, 
                    SET, DEL, TTL, KEYS, HSET)
from fastapi import FastAPI, Response
from memory_cache import MemoryCache

app = FastAPI()
cache = MemoryCache()
users = UsersData()


@app.post("/GET")
async def get(GET: GET) -> Response:
    if not users.check_token(GET.dict().get('token')):
        return 'Unauthorized'

    return await cache.get(
        GET.dict().get('key')
    )


@app.post("/SET")
async def set(SET: SET) -> Response:
    if not users.check_token(SET.dict().get('token')):
        return 'Unauthorized'

    return await cache.set(
        key=SET.dict().get('key'), 
        value=SET.dict().get('value'),
        ttl=SET.dict().get('ttl')
    )


@app.post("/DEL")
async def delete(DEL: DEL) -> Response:
    if not users.check_token(DEL.dict().get('token')):
        return 'Unauthorized'

    return await cache.delete(
        keys=DEL.dict().get('keys')
    )


@app.post('/SAVE')
async def save(SAVE: SAVE) -> Response:
    if not users.check_token(SAVE.dict().get('token')):
        return 'Unauthorized'

    return await cache.save()


@app.post('/TTL')
async def ttl(TTL: TTL) -> Response:
    if not users.check_token(TTL.dict().get('token')):
        return 'Unauthorized'

    return await cache.ttl(
        key=TTL.dict().get('key')
    )


@app.post('/KEYS')
async def keys(KEYS: KEYS) -> Response:
    if not users.check_token(KEYS.dict().get('token')):
        return 'Unauthorized'

    return await cache.keys(
        pattern=KEYS.dict().get('pattern')
    )


@app.post('/HSET')
async def hset(HSET: HSET) -> Response:
    if not users.check_token(HSET.dict().get('token')):
        return 'Unauthorized'

    return await cache.hset(
        key=HSET.dict().get('key'),
        fields=HSET.dict().get('fields')
    )


@app.post('/HGET')
async def hget(HGET: HGET) -> Response:
    if not users.check_token(HGET.dict().get('token')):
        return 'Unauthorized'

    return await cache.hget(
        key=HGET.dict().get('key'),
        field=HGET.dict().get('field')
    )


@app.post('/RPUSH')
async def rpush(RPUSH: RLPUSH) -> Response:
    if not users.check_token(RPUSH.dict().get('token')):
        return 'Unauthorized'

    return await cache.rpush(
        key=RPUSH.dict().get('key'),
        elements=RPUSH.dict().get('elements')
    )


@app.post('/LPUSH')
async def lpush(LPUSH: RLPUSH) -> Response:
    if not users.check_token(LPUSH.dict().get('token')):
        return 'Unauthorized'

    return await cache.lpush(
        key=LPUSH.dict().get('key'),
        elements=LPUSH.dict().get('elements')
    )


@app.post('/LSET')
async def lset(LSET: LSET) -> Response:
    if not users.check_token(LSET.dict().get('token')):
        return 'Unauthorized'

    return await cache.lset(
        key=LSET.dict().get('key'),
        index=LSET.dict().get('index'),
        element=LSET.dict().get('element')
    )


@app.post('/LGET')
async def lget(LGET: LGET) -> Response:
    if not users.check_token(LGET.dict().get('token')):
        return 'Unauthorized'

    return await cache.lget(
        key=LGET.dict().get('key'),
        index=LGET.dict().get('index')
    )


@app.post('/register')
async def register(Register: Register) -> Response:
    return await users.register(
        login=Register.dict().get('login'),
        password=Register.dict().get('password')
    )


@app.post('/auth')
async def auth(Auth: Auth) -> Response:
    return await users.auth(
        login=Auth.dict().get('login'),
        password=Auth.dict().get('password')
    )
