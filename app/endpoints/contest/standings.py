from fastapi import APIRouter, Depends
from starlette import status

from app.services import ProxyManager


router = APIRouter(
    prefix="/contests",
    tags=["standings"],
)


@router.get(
    "/{contest_id}/standings/my",
    status_code=status.HTTP_200_OK,
)
async def get_my_standings(
    contest_id: int,
    proxy_manager: ProxyManager = Depends(ProxyManager),
) -> dict:
    result = await proxy_manager.get_my_standing(contest_id)
    return result


@router.get(
    "/{contest_id}/standings",
    status_code=status.HTTP_200_OK,
)
async def get_contest_standings(
    contest_id: int,
    proxy_manager: ProxyManager = Depends(ProxyManager),
) -> dict:
    result = await proxy_manager.get_contest_standings(contest_id)
    return result
