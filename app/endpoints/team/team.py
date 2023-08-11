from fastapi import APIRouter, status
from starlette import status

from app.services import redis_storage_manager


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