from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from starlette import status

from app.schemas import TrainingSessionSchema
from app.services import TrainingSessionRepository, redis_storage_manager, training_manager
from app.utils import WebSocketMessage
from app.db.enums import MessageTypeEnum


router = APIRouter(
    prefix="/training-sessions",
    tags=["Training Sessions"],
)


@router.get(
    "/{training_session_id}",
    status_code=status.HTTP_200_OK,
)
async def get_training_session(
    training_session_id: str,
    training_session_repository: TrainingSessionRepository = Depends(),
) -> TrainingSessionSchema:
    training_session = await training_session_repository.get_training_session_by_id(
        training_session_id,
    )

    return TrainingSessionSchema.model_validate(training_session)


@router.get(
    "",
    status_code=status.HTTP_200_OK,
)
async def get_training_session(
    contest_external_id: str = Query(alias="contest_id"),
    team_external_id: str = Query(alias="team_id"),
    training_session_repository: TrainingSessionRepository = Depends(),
) -> TrainingSessionSchema:
    training_session = await training_session_repository.get_training_session(
        contest_external_id,
        team_external_id,
    )

    return TrainingSessionSchema.model_validate(training_session)


@router.post(
    "/{training_session_id}/complete",
    status_code=status.HTTP_200_OK,
)
async def complete_training_session(
    training_session_id: UUID,
    training_session_repository: TrainingSessionRepository = Depends(),
) -> TrainingSessionSchema:
    training_session = await training_session_repository.complete_training_session(
        training_session_id
    )

    response = TrainingSessionSchema.model_validate(training_session)

    message = WebSocketMessage(
        type=MessageTypeEnum.TRAINING_FINISHED,
        payload=None,
    )

    await training_manager.broadcast(str(training_session_id), message.json())

    return response


@router.get(
    "/{training_session_id}/code/{alias}",
    status_code=status.HTTP_200_OK,
)
async def get_code_from_redis(training_session_id: UUID, alias: str) -> dict:
    code = redis_storage_manager.codesnap.get(training_session_id, alias)
    return {"code": code}


@router.get(
    "/{training_session_id}/control/current",
    status_code=status.HTTP_200_OK,
)
async def get_current_controller(training_session_id: UUID) -> dict:
    user_id = redis_storage_manager.controller.get(training_session_id)
    return {"userId": user_id}


@router.get(
    "/{training_session_id}/online",
    status_code=status.HTTP_200_OK,
)
async def get_online_users(training_session_id: UUID) -> dict:
    users = redis_storage_manager.training_users.get_users(training_session_id)
    return {"users": users}