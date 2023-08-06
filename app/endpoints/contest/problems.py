from fastapi import APIRouter, Depends
from starlette import status

from app.services import ProxyManager


router = APIRouter(
    prefix="/contests",
    tags=["standings"],
)


@router.get(
    "/{contest_id}/problems",
    status_code=status.HTTP_200_OK,
)
async def contest_problems(
    contest_id: int,
    proxy_manager: ProxyManager = Depends(ProxyManager),
) -> dict:
    result = await proxy_manager.get_contest_problems(contest_id)
    return result
