from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from app.db.connection import get_session
from app.schemas import PingResponse
from app.utils.health_check import health_check_db
from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter(
    prefix="/health_check",
    tags=["Application Health"],
)


@router.get(
    "/ping_application",
    response_model=PingResponse,
    status_code=status.HTTP_200_OK,
)
async def ping_application() -> dict:
    return {"message": "Application worked!"}


@router.get(
    "/ping_database",
    response_model=PingResponse,
    status_code=status.HTTP_200_OK,
    responses={status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Database isn't working"}},
)
async def ping_database(
    session: AsyncSession = Depends(get_session),
) -> dict:
    if await health_check_db(session):
        return {"message": "Database worked!"}
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Database isn't working",
    )
