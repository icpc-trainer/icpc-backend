import json
from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from app.services import (
    ProxyManager,
    UserRepository,
    TrainingSessionRepository,
    ProblemRepository,
    CommentRepository,
    training_manager,
)
from app.schemas import CommentSchema, CommentRequest
from app.utils import WebSocketMessage
from app.db.enums import MessageTypeEnum


router = APIRouter(
    prefix="/training-sessions",
    tags=["comment"],
)


@router.post(
    "/{training_session_id}/problem/{problem_alias}/comment/send",
    status_code=status.HTTP_200_OK,
)
async def send_problem_comment(
    training_session_id: str,
    problem_alias: str,
    body: CommentRequest,
    proxy_manager: ProxyManager = Depends(ProxyManager),
    user_repository: UserRepository = Depends(),
    training_session_repository: TrainingSessionRepository = Depends(),
    problem_repository: ProblemRepository = Depends(),
    comment_repository: CommentRepository = Depends(),
) -> CommentSchema:
    # получение информации о пользователе
    user_data = await proxy_manager.get_me()
    user = await user_repository.get_user_by_external_id(user_data.get("id"))
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    # получение id контеста
    training_session = await training_session_repository.get_training_session_by_id(training_session_id)
    contest_id = training_session.contest.id

    # получение задачи по contest_id и problem_alias
    problem = await problem_repository.get_problem_by_contest_id_and_alias(
        contest_id=contest_id,
        problem_alias=problem_alias
    )
    if not problem:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    # создание коммента
    comment = await comment_repository.create_comment(
        user_id=user.id,
        problem_id=problem.id,
        training_session_id=training_session.id,
        content=body.content
    )

    # отправка коммента по сокету
    message = WebSocketMessage(
        MessageTypeEnum.PROBLEM_COMMENT_RECEIVED,
        {
            "id": str(comment.id),
            "userId": user_data.get("id"),
            "userFirstName": user_data.get("first_name"),
            "userLastName": user_data.get("last_name"),
            "userLogin": user_data.get("login"),
            "problemAlias": problem_alias,
            "content": body.content,
            "dtCreated": str(comment.dt_created)
        }
    )
    await training_manager.broadcast(training_session_id, message.json())

    return CommentSchema.model_validate_json(json.dumps(message.payload))


