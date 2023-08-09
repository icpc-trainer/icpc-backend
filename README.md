### Openapi
Formal description of the OpenAPI 3.0 interface here [openapi.json](./openapi.json)

### Run
- `make env`
- `docker-compose up --build`
- Then check `localhost:8000/docs`


### Вэб сокеты

#### Лобби

`ws://localhost:8000/ws/lobby`


| Параметр       |                |
|----------------|----------------|
| team_id        | id команды     |
| user_id        | id пользователя|

Пример:
~~~~
ws://localhost:8000/ws/lobby?team_id=12&user_id=1
~~~~

Кол-во одновременных соединений ограничено, по дефолту 3.
При превышении возвращается ошибка с кодом 1008.


#### Тренировка

`ws://localhost:8000/ws/training`


| Параметр            |                    |
|---------------------|--------------------|
| training_session_id | id сессии          |
| user_id             | id пользователя    |

Пример:
~~~~
ws://localhost:8000/ws/training?training_session_id=1&user_id=2
~~~~

Кол-во одновременных соединений ограничено, по дефолту 3.
При превышении возвращается ошибка с кодом 1008.

---

Типы сообщения

| Тип сообщения       | Значение                 |
|---------------------|--------------------------|
| USER_JOIN           | Когда кто-то подключился |
| USER_LEAVE          | Когда кто-то отключился  |

Шаблон сообщения

~~~~json
{
    "type": "USER_JOIN",
    "payload": {}
}
~~~~