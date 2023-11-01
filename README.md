# ICPC-Trainer
> Проект реализован в рамках 2ого этапа Летних Школ Яндекса<br>
> <img height="350" src="https://github.com/icpc-trainer/static/blob/master/team1.png"><br>
> Команда бэкенда: [Асланбек](https://github.com/slonoboy), [Максим](https://github.com/exynil), [Сергей](https://peskov.dev/)<br>
> Фронтенд проекта: https://github.com/icpc-trainer/icpc-frontend<br>

ICPC-Trainer - Веб-сервис на базе Яндекс Контест, максимально точно эмулирующий механику проведения соревнований ICPC.
Сервис помогает проводить тренировки по спортивному программированию онлайн.


### Api documentation
- OpenAPI 3.0: [openapi.json](./openapi.json)
- Websockets: [websocket_api.md](./websocket_api.md)

### Run
- `make env`
- `docker-compose up --build`
- Then check `localhost:8000/docs`

### Presentation
[<img src="https://github.com/icpc-trainer/static/blob/master/play.png">](https://www.youtube.com/embed/ijCNsuOVu0Q)

| Backend                                                                         |
|---------------------------------------------------------------------------------|
| <img src="https://github.com/icpc-trainer/static/blob/master/workflow.png">     |
| <img src="https://github.com/icpc-trainer/static/blob/master/architecture.png"> |

| Yandex Contest API: https://api.contest.yandex.net/api/public/swagger-ui.html#/        |
|----------------------------------------------------------------------------------------|
| <img src="https://github.com/icpc-trainer/static/blob/master/contest_integration.png"> |

| Websockets                                                                   |
|------------------------------------------------------------------------------|
| <img src="https://github.com/icpc-trainer/static/blob/master/websocket.png"> |
