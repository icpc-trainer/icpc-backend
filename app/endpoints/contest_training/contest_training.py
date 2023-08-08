from uuid import UUID

from fastapi import APIRouter, Depends, Query
from starlette import status

from app.schemas import ContestTrainingSchema
from app.services import ContestTrainingRepository


router = APIRouter(
    prefix="/contest-trainings",
    tags=["Contest Trainings"],
)


@router.get(
    "",
    status_code=status.HTTP_200_OK,
)
async def get_contest_training(
    contest_external_id: str = Query(alias="contest_id"),
    team_external_id: str = Query(alias="team_id"),
    contest_training_repository: ContestTrainingRepository = Depends(),
) -> ContestTrainingSchema:
    contest_training = await contest_training_repository.get_contest_training(
        contest_external_id,
        team_external_id,
    )

    return ContestTrainingSchema.model_validate(contest_training)


@router.post(
    "/{contest_training_id}/complete",
    status_code=status.HTTP_200_OK,
)
async def complete_contest_training(
    contest_training_id: UUID,
    contest_training_repository: ContestTrainingRepository = Depends(),
) -> ContestTrainingSchema:
    contest_training = await contest_training_repository.complete_contest_training(
        contest_training_id
    )

    return ContestTrainingSchema.model_validate(contest_training)
