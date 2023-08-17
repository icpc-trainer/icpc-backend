### Openapi
Formal description of the OpenAPI 3.0 interface here [openapi.json](./openapi.json)

### Run
- `make env`
- `docker-compose up --build`
- Then check `localhost:8000/docs`


### Вэб сокеты

#### Лобби

`ws://localhost:8000/ws/lobby`


| Параметр       |         |
|----------------|---------|
| team_id        | int     |
| user_id        | int     |

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
| training_session_id | UUID               |
| user_id             | int                |

Пример:
~~~~
ws://localhost:8000/ws/training?training_session_id=04d3f707-ed68-4b2d-a91a-0ae200c5c7d3&user_id=2
~~~~

Кол-во одновременных соединений ограничено, по дефолту 3.
При превышении возвращается ошибка с кодом 1008.

---

### Типы сообщения

`USER_JOIN` - отправляется всем когда кто-то подключается

`USER_LEAVE` - отправляется всем когда кто-то отключается

`SUBMISSION_VERDICT_RETRIEVED` - [не задокументировано]

`SUBMISSION_VERDICT_PENDING` - [не задокументировано]

`CODE_EDITOR_UPDATE` - обновилось состояние редактора кода

Этот тип сообщения прослушивается. Сохраняется содержимое редактора кода

Обязательные поля в `payload`: `code`, `problemALias`
~~~~json
{
    "type": "CODE_EDITOR_UPDATE",
    "payload": {
        "code": "print('hello')",
        "problemAlias": "A"
    }
}
~~~~

`CONTROL_TAKEN` - изменился управляющий редактором кода

Этот тип сообщения прослушивается. Сохраняется информация о том кто взял управление над редактором кода

Обязательные поля в `payload`: `userId`
~~~~json
{
    "type": "CONTROL_TAKEN",
    "payload": {
        "userId": "823768129",
    }
}
~~~~

`TRAINING_STARTED` - отправляется всем когда кто-то нажал кнопку начала тренировки

~~~~json
{
    "type": "TRAINING_STARTED",
    "payload": {
        "id": "0fc88187-cd79-473b-be37-05e2e475abb6",
        "status": "IN_PROCESS",
        "dtCreated": "2023-08-17 17:50:09.378486+00:00"
    }
}
~~~~

`TRAINING_FINISHED` - отправляется всем когда кто-то нажал кнопку завершения тренировки

~~~~json
{
    "type": "TRAINING_FINISHED",
    "payload": null
}
~~~~

`USER` - информация о пользователе

Этот тип сообщения прослушивается. Сохраняется информация о пользователе

Обязательные поля в `payload`: `user`
~~~~json
{
    "type": "USER",
    "payload": {
        "user": "<информация_о_пользователе>",
    }
}
~~~~


`PROBLEM_ASSIGNED` - назначение задачи пользователю

Этот тип сообщения прослушивается. Сохраняется информация о пользователе

Обязательные поля в `payload`: `user`, `problemAlias`
~~~~json
{
    "type": "PROBLEM_ASSIGNED",
    "payload": {
        "user": "<информация_о_пользователе>",
        "problemAlias": "B",
    }
}
~~~~