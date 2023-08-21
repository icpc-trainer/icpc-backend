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
    "payload": {
        "id": "0fc88187-cd79-473b-be37-05e2e475abb6",
        "teamId": "0fc88187-cd79-473b-be37-05e2e475abb6",
        "contestId": "0fc88187-cd79-473b-be37-05e2e475abb6",
        "status": "FINISHED",
    }
}
~~~~

`CONTEST_FINISHED` - отправляется всем когда время контеста истекло

~~~~json
{
    "type": "CONTEST_FINISHED",
    "payload": {
        "id": "0fc88187-cd79-473b-be37-05e2e475abb6",
        "teamId": "0fc88187-cd79-473b-be37-05e2e475abb6",
        "contestId": "0fc88187-cd79-473b-be37-05e2e475abb6",
        "status": "FINISHED",
    }
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

`CONTEST_SELECTED` - выбор контеста в лобби

Этот тип сообщения прослушивается. Сохраняется информация о выбранном контесте

Обязательные поля в `payload`: `contestId`
~~~~json
{
    "type": "CONTEST_SELECTED",
    "payload": {
        "contestId": 51004,
    }
}
~~~~

`PROBLEM_ATTEMPTS_UPDATED` - обновление кол-во попыток по задаче
~~~~json
{
    "type": "PROBLEM_ATTEMPTS_UPDATED",
    "payload": {
        "attempts": 3,
        "problemAlias": "A"
    }
}
~~~~

`COMPILER_SELECTED` - изменение компилятора

Этот тип сообщения прослушивается. Сохраняется информация о выбранном компиляторе

Обязательные поля в `payload`: `compiler`, `problemAlias`
~~~~json
{
    "type": "COMPILER_SELECTED",
    "payload": {
        "compiler": "python3_docker",
        "problemAlias": "B",
    }
}
~~~~

`PROBLEM_COMMENT_RECEIVED` - Коммент отправляется по ручке, событие тригерит вебсокет
~~~~json
{
    "type": "PROBLEM_COMMENT_RECEIVED",
    "payload": {
        "id": "63717229-f397-4bf9-9d9b-3d44005a5dd2",
        "userId": 1764832810,
        "userFirstName": "John",
        "userLastName": "Doe",
        "userLogin": "johoe",
        "problemAlias": "A",
        "content": "Content of comment",
        "dtCreated": "2023-08-17 17:50:09.378486+00:00",
    }
}
~~~~

`PROBLEM_COMMENT_UPDATED` - Коммент обновляется по ручке, событие тригерит вебсокет
~~~~json
{
    "type": "PROBLEM_COMMENT_UPDATED",
    "payload": {
        "id": "63717229-f397-4bf9-9d9b-3d44005a5dd2",
        "userId": 1764832810,
        "userFirstName": "John",
        "userLastName": "Doe",
        "userLogin": "johoe",
        "problemAlias": "A",
        "content": "New content of comment",
        "dtCreated": "2023-08-17 17:50:09.378486+00:00",
    }
}
~~~~

`PROBLEM_COMMENT_DELETED` - Коммент удаляется по ручке, событие тригерит вебсокет
~~~~json
{
    "type": "PROBLEM_COMMENT_DELETED",
    "payload": {
        "id": "63717229-f397-4bf9-9d9b-3d44005a5dd2",
    }
}
~~~~
