from uuid import UUID

from fastapi import Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.connection import get_session
from app.db.enums import TrainingStatusEnum
from app.db.models import User


class UserRepository:
    def __init__(self, session: AsyncSession = Depends(get_session)):
        self.session = session

    async def create_user_if_not_exists(
        self,
        user_data: dict,
    ) -> User:
        query = select(User).where(User.external_id==user_data.get("id"))
        user = await self.session.scalar(query)
        if not user:
            user = User(
                external_id=user_data.get("id"),
                login=user_data.get("login"),
                first_name=user_data.get("first_name"),
                last_name=user_data.get("last_name"),
            )
            self.session.add(user)
            await self.session.commit()
            await self.session.refresh(user)

        return user
