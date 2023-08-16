from fastapi import APIRouter, status, Depends
from starlette import status

from app.services import redis_storage_manager, ProxyManager, TeamManager


router = APIRouter(
    prefix="/teams",
    tags=["Teams"],
)


@router.get(
    "/{team_id}/online",
    status_code=status.HTTP_200_OK,
)
async def get_online_users(team_id: str) -> dict:
    users = redis_storage_manager.lobby_users.get_users(team_id)
    return {"users": users}


@router.get(
    "",
    status_code=status.HTTP_200_OK,
)
async def get_user_teams(
    proxy_manager: ProxyManager = Depends(ProxyManager),
    team_manager: TeamManager = Depends()
) -> tuple:
    teams = await proxy_manager.get_user_teams()
    # TODO должны ли удалять команды если на контесте они удаляются?
    if teams:
        await team_manager.init_teams(teams)
    return teams
