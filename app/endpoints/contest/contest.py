from fastapi import APIRouter, Depends
from starlette import status

from app.services import ProxyManager, ContestRepository


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

