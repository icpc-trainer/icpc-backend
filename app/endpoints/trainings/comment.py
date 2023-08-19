import json
from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from typing import List

from app.services import (
    ProxyManager,
    UserRepository,
    TrainingSessionRepository,
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
    "/{training_session_id}/problem/{problem_alias}/comments/send",
    status_code=status.HTTP_200_OK,
)
async def send_problem_comment(
    training_session_id: str,
    problem_alias: str,
    body: CommentRequest,
    proxy_manager: ProxyManager = Depends(ProxyManager),
    user_repository: UserRepository = Depends(),
    training_session_repository: TrainingSessionRepository = Depends(),
    comment_repository: CommentRepository = Depends(),
) -> CommentSchema:
    # получение информации о пользователе
    user_data = await proxy_manager.get_me()
    user = await user_repository.get_user_by_external_id(user_data.get("id"))
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    # получение id training_session
    training_session = await training_session_repository.get_training_session_by_id(
        training_session_id
    )

    # создание коммента
    comment = await comment_repository.create_comment(
        user_id=user.id,
        training_session_id=training_session.id,
        problem_alias=problem_alias,
        content=body.content,
    )

    # отправка коммента по сокету
    message = WebSocketMessage(
        type=MessageTypeEnum.PROBLEM_COMMENT_RECEIVED,
        payload={
            "id": str(comment.id),
            "userId": user_data.get("id"),
            "userFirstName": user_data.get("first_name"),
            "userLastName": user_data.get("last_name"),
            "userLogin": user_data.get("login"),
            "problemAlias": problem_alias,
            "content": body.content,
            "dtCreated": str(comment.dt_created),
        },
    )
    await training_manager.broadcast(training_session_id, message.json())

    return CommentSchema.model_validate_json(json.dumps(message.payload))


@router.get(
    "/{training_session_id}/problem/{problem_alias}/comments",
    status_code=status.HTTP_200_OK,
)
async def get_problem_comments(
    training_session_id: str,
    problem_alias: str,
    comment_repository: CommentRepository = Depends(),
) -> List[CommentSchema]:
    comments = await comment_repository.get_comments(
        training_session_id=training_session_id,
        problem_alias=problem_alias,
    )
    result = []
    for comment in comments:
        result.append(
            CommentSchema(
                id=comment.id,
                userId=comment.user.external_id,
                userFirstName=comment.user.first_name,
                userLastName=comment.user.last_name,
                userLogin=comment.user.login,
                problemAlias=comment.problem_alias,
                content=comment.content,
                dtCreated=comment.dt_created,
            )
        )
    return result
