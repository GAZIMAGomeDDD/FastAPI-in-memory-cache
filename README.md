# Тестовое задание Avito в юнит Geo

Программа реализованная с помощью FastAPI.

## Установка

1. Для установки необходимо склонировать репозиторий:
```bash
git clone https://github.com/gazik05/FastAPI-memory-cache
```
2. Вводим команду для создания docker образов:
```bash
docker-compose build
```
3. Как только образы будут собраны, запускаем контейнеры командой::
```bash
docker-compose up -d
```
4. Смотрим логи:
```bash
docker-compose logs -f
```
5. Для приостановки docker контейнеров используйте команду:
```bash
docker-compose down
```

### Методы
|Метод HTTP|URL|Действие|
|---|---|---|
|POST|/register|Регистрация пользователя: <login, password>|
|POST|/auth|Аутентификация пользователя: <login, password>|
|POST|/SET|Метод SET (создает key-value объект, опционально можно установить ttl): <key, value, token, Optional[ttl]>|
|POST|/TTL|Метод TTL (если ключ установлен с истечением срока действия, эту команду можно использовать для просмотра оставшегося времени): <key>|
|POST|/GET|Метод GET (получает value по указаному ключу): <key>|
|POST|/HSET|Метод HSET (создает hash объект): <key, field, value, token>|
|POST|/HGET|Метод HGET (получает value по указаному ключу и полю): <key, field, token>|
|POST|/RPUSH|Метод RPUSH (создает новый список, если список с таким ключем существует, добаляет элементы справа): <key, elements, token>|
|POST|/LPUSH|Метод RPUSH (создает новый список, если список с таким ключем существует, добаляет элементы слева): <key, elements, token>|
|POST|/LSET|Метод LSET (заменяет элемент в списке на новый): <key, index, element, token>|
|POST|/LGET|Метод LGET (получает элемент списка по индексу и ключу): <key, index, token>|
|POST|/KEYS|Метод KEYS (возвращает все ключи по указанному шаблону): <pattern, token>|
|POST|/DEL|Метод DEL (удаляет ключи и соответствующее их значения): <keys, token>|
|POST|/SAVE|Метод SAVE (Создает дамп данных)|

### Документация доступна по адресу [http://127.0.0.1:8000/docs]

### Примеры запросов

#### Register
```
$ curl -X POST "http://127.0.0.1:8000/register" -H "accept: application/json" -H  "Content-Type: application/json" -d '{"login": "robin", "password": "good"}'

response: "OK"

```

#### Auth
```
$ curl -X POST "http://127.0.0.1:8000/auth" -H "accept: application/json" -H  "Content-Type: application/json" -d '{"login": "robin", "password": "good"}'

response: "0k1KyNsiSl" (рандомно сгенерированный токен)

```

#### SET
```
$ curl -X POST "http://127.0.0.1:8000/SET" -H "accept: application/json" -H  "Content-Type: application/json" -d '{"key": "GB", "value": "London", "token": "0k1KyNsiSl"}'

response: "OK"

```

#### GET
```
$ curl -X POST "http://127.0.0.1:8000/GET" -H "accept: application/json" -H  "Content-Type: application/json" -d '{"key": "GB", "token": "0k1KyNsiSl"}'

response: "London"

```


#### SET(с установленным TTL)
```
$ curl -X POST "http://127.0.0.1:8000/SET" -H "accept: application/json" -H  "Content-Type: application/json" -d '{"key": "Russia", "value": "Moscow", "token": "0k1KyNsiSl", "ttl": 10}'

response: "OK"

```

#### TTL
```
$ curl -X POST "http://127.0.0.1:8000/SET" -H "accept: application/json" -H  "Content-Type: application/json" -d '{"key": "Russia", "token": "0k1KyNsiSl"}'

response: sec

```

#### HSET
```
$ curl -X POST "http://127.0.0.1:8000/HSET" -H "accept: application/json" -H  "Content-Type: application/json" -d '{"key": "family", "fields": [{"key": "dad", "value": "John"}, {"key": "mom", "value": "Anna"}, {"key": "son", "value": "Sam"}], "token": "0k1KyNsiSl"}'

response: 3

```
```
$ curl -X POST "http://127.0.0.1:8000/HSET" -H "accept: application/json" -H  "Content-Type: application/json" -d '{"key": "family", "fields": [{"key": "daughter", "value": "Jenna"}], "token": "0k1KyNsiSl"}'

response: 1

```
```
$ curl -X POST "http://127.0.0.1:8000/HSET" -H "accept: application/json" -H  "Content-Type: application/json" -d '{"key": "family", "fields": [{"key": "son", "value": "Anthony"}], "token": "0k1KyNsiSl"}'

response: 0

```

#### RPUSH
```
$ curl -X POST "http://127.0.0.1:8000/RPUSH" -H "accept: application/json" -H  "Content-Type: application/json" -d '{"key": "digits", "elements": [1, 2, 3, 4, 5], "token": "0k1KyNsiSl"}'

response: 5

```

#### LPUSH
```
$ curl -X POST "http://127.0.0.1:8000/LPUSH" -H "accept: application/json" -H  "Content-Type: application/json" -d '{"key": "digits", "elements": [-5, -4, -3, -2, -1, 1], "token": "0k1KyNsiSl"}'

response: 11

```

#### LSET
```
$ curl -X POST "http://127.0.0.1:8000/LSET" -H "accept: application/json" -H  "Content-Type: application/json" -d '{"key": "digits", "index": 5, "element": 0, "token": "0k1KyNsiSl"}'

response: "OK"

```

#### LGET
```
$ curl -X POST "http://127.0.0.1:8000/LGET" -H "accept: application/json" -H  "Content-Type: application/json" -d '{"key": "digits", "index": 5, "token": "0k1KyNsiSl"}'

response: 0

```

#### KEYS
```
$ curl -X POST "http://127.0.0.1:8000/KEYS" -H "accept: application/json" -H  "Content-Type: application/json" -d '{"pattern": "[a-zA-Z_][a-zA-Z0-9_]", "token": "0k1KyNsiSl"}'

response: ["GB", "family", "digits"]

```

#### SAVE
```
$ curl -X POST "http://127.0.0.1:8000/SAVE" -H "accept: application/json" -H  "Content-Type: application/json" -d '{"token": "0k1KyNsiSl"}'

response: "OK"

```

#### DEL
```
$ curl -X POST "http://127.0.0.1:8000/DEL" -H "accept: application/json" -H  "Content-Type: application/json" -d '{"keys": ["GB", "family", "digits"], "token": "0k1KyNsiSl"}'

response: 3

```
