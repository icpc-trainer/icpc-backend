from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.db.connection import get_session
from app.schemas import PingResponse
from app.services import ContestApiManager
from app.utils.health_check import health_check_db


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
    contest_api_manager: Annotated[ContestApiManager, Depends(ContestApiManager)],
) -> dict:
    result = await contest_api_manager.get_my_standing(contest_id)
    return result
