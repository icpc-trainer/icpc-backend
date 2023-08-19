from fastapi import APIRouter, Depends
from starlette import status

from app.services import ProxyManager, ContestRepository
from app.schemas import ContestSchema


router = APIRouter(
    prefix="/contests",
    tags=["contest"],
)


@router.get(
    "/{training_session_id}",
    status_code=status.HTTP_200_OK,
)
async def contest_data(
    training_session_id: str,
    proxy_manager: ProxyManager = Depends(ProxyManager),
) -> dict:
    contest_data = await proxy_manager.get_contest(training_session_id)
    return contest_data

@router.get(
    "",
    status_code=status.HTTP_200_OK,
)
async def get_contests(
    contest_repository: ContestRepository = Depends(),
) -> list[ContestSchema]:
    # # TODO исправить этот говнокод
    contests = await contest_repository.get_all()
    response = []

    for contest in contests:
        response.append(
            ContestSchema(
                id=contest.external_id,
                name=contest.name
            )
        )
    return response