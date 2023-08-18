from fastapi import APIRouter, Depends, status

from app.services import RedisStorageManager


router = APIRouter(
    prefix="/lobby",
    tags=["Lobby"],
)


@router.get(
    "/{team_id}/online",
    status_code=status.HTTP_200_OK,
)
async def get_online_users(
    team_id: str,
    redis_storage_manager: RedisStorageManager = Depends(),
) -> dict:
    users = redis_storage_manager.lobby_users.get_users(team_id)
    return {"users": users}


@router.get(
    "/{team_id}/selected-contest",
    status_code=status.HTTP_200_OK,
)
async def get_selected_contest(
    team_id: str,
    redis_storage_manager: RedisStorageManager = Depends(),
) -> dict:
    contest_id = redis_storage_manager.selected_contests.get(team_id)
    return {"contestId": contest_id}
