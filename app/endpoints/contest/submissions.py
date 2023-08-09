import json
from fastapi import APIRouter, Depends, File, Form, UploadFile, Security, BackgroundTasks
from fastapi.security.api_key import APIKeyHeader
from starlette import status

from app.services import ProxyManager
from app.background_tasks import get_submission_verdict
from app.services import training_manager
from app.db.enums import MessageTypeEnum


router = APIRouter(
    prefix="/contests",
    tags=["standings"],
)


@router.post(
    "/{contest_id}/submissions",
    status_code=status.HTTP_200_OK,
)
async def submit_solution(
    background_tasks: BackgroundTasks,
    contest_id: int,
    file: UploadFile = File(...),
    compiler: str = Form(...),
    problem: str = Form(...),
    training_session_id: str = Form(...),
    proxy_manager: ProxyManager = Depends(ProxyManager),
    oauth_token: str = Security(APIKeyHeader(name="Authorization")),
) -> dict:
    # уведомление об отправке ответа на задачу в websocket каналe
    message = {
        "type": MessageTypeEnum.SUBMISSION_VERDICT_PENDING,
        "data": {},
    }
    await training_manager.broadcast(json.dumps(message), training_session_id)

    # отправка ответа на задачу в контест апи и получение runId
    result = await proxy_manager.submit_solution(
        contest_id,
        problem,
        compiler,
        file,
    )

    # создание фоновой задачи на мониторинг вердикта отправки
    submission_id = result.get("runId")
    background_tasks.add_task(
        get_submission_verdict,
        oauth_token,
        contest_id,
        submission_id,
        training_session_id,
    )
    return result
