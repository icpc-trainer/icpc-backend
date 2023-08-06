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



#### Тренировка

`ws://localhost:8000/ws/training`


| Параметр       |                    |
|----------------|--------------------|
| team_id        | id команды         |
| contest_id     | id контеста        |
| user_id        | id пользователя    |

Пример:
~~~~
ws://localhost:8000/ws/training?team_id=12&contest_id=68&user_id=1
~~~~

