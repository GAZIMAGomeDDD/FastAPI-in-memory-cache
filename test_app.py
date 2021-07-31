import time

from fastapi.testclient import TestClient
from api import app
from string import ascii_uppercase, ascii_lowercase, digits
from random import sample

client = TestClient(app)


def random_text() -> str:
    return ''.join(sample(ascii_uppercase + ascii_lowercase + digits, 10))


login = random_text()
password = random_text()


def get_token() -> str:
    response = client.post("/auth", json={
        "login": login,
        "password": password
    })

    return response.json()


def test_register():
    response = client.post("/register", json={
        "login": login,
        "password": password
    })

    assert response.status_code == 200
    assert response.json() == 'OK'


def test_auth():
    response = client.post("/auth", json={
        "login": login,
        "password": password
    })

    assert response.status_code == 200
    assert response.json() != 'Login not found'
    assert response.json() != 'Password mismatch'


def test_set_method():
    response = client.post("/SET", json={
        "key": "Apple",
        "value": "iphone 15",
        "token": get_token()
    })

    assert response.status_code == 200
    assert response.json() == 'OK'


def test_get_method():
    response = client.post("/GET", json={
        "key": "Apple",
        "token": get_token()
    })

    assert response.status_code == 200
    assert response.json() == 'iphone 15'


def test_set_method_with_ttl():
    set_response = client.post("/SET", json={
        "key": "Samsung",
        "value": "Galaxy s9",
        "ttl": 10,
        "token": get_token()
    })

    assert set_response.status_code == 200
    assert set_response.json() == 'OK'

    time.sleep(5)

    first_ttl_response = client.post("/TTL", json={
        "key": "Samsung",
        "token": get_token()
    })

    assert first_ttl_response.status_code == 200
    assert first_ttl_response.json() == 5

    first_get_response = client.post("/GET", json={
        "key": "Samsung",
        "token": get_token()
    })

    assert first_get_response.status_code == 200
    assert first_get_response.json() == 'Galaxy s9'

    time.sleep(6)

    second_ttl_response = client.post("/TTL", json={
        "key": "Samsung",
        "token": get_token()
    })

    assert second_ttl_response.status_code == 200
    assert second_ttl_response.json() == -2

    second_get_response = client.post("/GET", json={
        "key": "Samsung",
        "token": get_token()
    })

    assert second_get_response.status_code == 200
    assert second_get_response.json() == None


def test_hset_method():
    first_response = client.post("/HSET", json={
        "key": "family",
        "fields": [
            {
                "key": "dad",
                "value": "John"
            },
            {
                "key": "mom",
                "value": "Anna"
            },
            {
                "key": "son",
                "value": "Sam"
            }
        ],
        "token": get_token()
    })

    assert first_response.status_code == 200
    assert first_response.json() == 3

    second_response = client.post("/HSET", json={
        "key": "family",
        "fields": [
            {
                "key": "daughter",
                "value": "Jenna"
            }
        ],
        "token": get_token()
    })

    assert second_response.status_code == 200
    assert second_response.json() == 1

    third_response = client.post("/HSET", json={
        "key": "family",
        "fields": [
            {
                "key": "son",
                "value": "Anthony"
            }
        ],
        "token": get_token()
    })

    assert third_response.status_code == 200
    assert third_response.json() == 0


def test_hget_method():
    first_response = client.post("/HGET", json={
        "key": "family",
        "field": "son",
        "token": get_token()
    })

    assert first_response.status_code == 200
    assert first_response.json() == "Anthony"

    second_response = client.post("/HGET", json={
        "key": "family",
        "field": "grandma",
        "token": get_token()
    })

    assert second_response.status_code == 200
    assert second_response.json() == None

    third_response = client.post("/HGET", json={
        "key": "Apple",
        "field": "iphone",
        "token": get_token()
    })

    assert third_response.status_code == 200
    assert third_response.json() == 'WRONGTYPE Operation against a key holding the wrong kind of value'

    
def test_rpush_method():
    first_response = client.post("/RPUSH", json={
        "key": "digits", 
        "elements": [1, 2, 3, 4, 5], 
        "token": get_token()
    })

    assert first_response.status_code == 200
    assert first_response.json() == 5

    second_response = client.post("/RPUSH", json={
        "key": "Apple",
        "elements": [1, 2, 3, 4, 5], 
        "token": get_token()
    })

    assert second_response.status_code == 200
    assert second_response.json() == 'WRONGTYPE Operation against a key holding the wrong kind of value'


def test_lpush_method():
    first_response = client.post("/LPUSH", json={
        "key": "digits", 
        "elements": [-5, -4, -3, -2, -1, 1], 
        "token": get_token()
    })

    assert first_response.status_code == 200
    assert first_response.json() == 11

    second_response = client.post("/LPUSH", json={
        "key": "family",
        "elements": [-5, -4, -3, -2, -1, 1], 
        "token": get_token()
    })

    assert second_response.status_code == 200
    assert second_response.json() == 'WRONGTYPE Operation against a key holding the wrong kind of value'


def test_lset_method():
    first_response = client.post("/LSET", json={
        "key": "digits",
        "index": 5,
        "element": 0, 
        "token": get_token()
    })

    assert first_response.status_code == 200
    assert first_response.json() == "OK"

    second_response = client.post("/LSET", json={
        "key": "digits",
        "index": 11,
        "element": 6, 
        "token": get_token()
    })

    assert second_response.status_code == 200
    assert second_response.json() == 'ERR index out of range'

    third_response = client.post("/LSET", json={
        "key": "family",
        "index": 11,
        "element": 6, 
        "token": get_token()
    })

    assert third_response.status_code == 200
    assert third_response.json() == 'WRONGTYPE Operation against a key holding the wrong kind of value'

    fourth_response = client.post("/LSET", json={
        "key": "blablablabla",
        "index": 12121,
        "element": 'blablablabla', 
        "token": get_token()
    })

    assert fourth_response.status_code == 200
    assert fourth_response.json() == 'ERR no such key'


def test_lget_method():
    first_response = client.post("/LGET", json={
        "key": "digits",
        "index": 5,
        "token": get_token()
    })

    assert first_response.status_code == 200
    assert int(first_response.json()) == 0

    second_response = client.post("/LGET", json={
        "key": "digits",
        "index": 11,
        "token": get_token()
    })

    assert second_response.status_code == 200
    assert second_response.json() == None


def test_keys_method():
    response = client.post("/KEYS", json={
        "pattern": "[a-zA-Z_][a-zA-Z0-9_]", 
        "token": get_token()
    })

    assert response.status_code == 200
    assert response.json() == ['Apple', 'family', 'digits']

    
def test_del_method():
    response = client.post("/DEL", json={
        "keys": ['Apple', 'family', 'digits'], 
        "token": get_token()
    })

    assert response.status_code == 200
    assert response.json() == 3


def test_save_method():
    response = client.post("/SAVE", json={
        "token": get_token()
    })

    assert response.status_code == 200
    assert response.json() == "OK"
