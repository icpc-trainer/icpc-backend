from fastapi import APIRouter, Depends, Form
from starlette import status

from app.services import ProxyManager, UserRepository


router = APIRouter(
    prefix="/user",
    tags=["user"],
)


@router.get(
    "/me",
    status_code=status.HTTP_200_OK,
)
async def get_me(
    proxy_manager: ProxyManager = Depends(ProxyManager),
    user_repository: UserRepository = Depends()
) -> dict:
    user_data = await proxy_manager.get_me()
    await user_repository.create_user_if_not_exists(user_data)

    return user_data
