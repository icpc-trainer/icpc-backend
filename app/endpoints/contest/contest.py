from fastapi import APIRouter, Depends
from starlette import status

from app.services import ProxyManager, ContestRepository
from app.schemas import ContestSchema


router = APIRouter(
    prefix="/contests",
    tags=["contest"],
)


@router.get(
    "/{contest_id}",
    status_code=status.HTTP_200_OK,
)
async def contest_data(
    contest_id: int,
    proxy_manager: ProxyManager = Depends(ProxyManager),
    contest_repository: ContestRepository = Depends(),
) -> dict:
    contest_data = await proxy_manager.get_contest(contest_id)
    await contest_repository.create_if_not_exists(
        str(contest_id),
        contest_data,
    )
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