from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from starlette import status

from app.schemas import TrainingSessionSchema
from app.services import TrainingSessionRepository, redis_storage_manager


router = APIRouter(
    prefix="/training-sessions",
    tags=["Training Sessions"],
)


@router.get(
    "/{training_session_id}",
    status_code=status.HTTP_200_OK,
)
async def get_training_session(
    training_session_id: UUID,
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

    return TrainingSessionSchema.model_validate(training_session)


@router.get(
    "/{training_session_id}/code/{alias}",
    status_code=status.HTTP_200_OK,
)
async def get_code_from_redis(training_session_id: UUID, alias: str):
    return redis_storage_manager.codesnap.get(training_session_id, alias)
