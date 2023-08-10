from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.connection import get_session
from app.db.models import Contest


class ContestRepository:
    def __init__(self, session: AsyncSession = Depends(get_session)):
        self.session = session

    async def get_contest_by_external_id(
        self,
        contest_external_id: str,
    ) -> Contest:
        query = select(Contest).where(
            Contest.external_id==contest_external_id,
        )
        return await self.session.scalar(query)

    async def create_if_not_exists(
        self,
        contest_external_id: str,
        contest_data: dict,
    ) -> Contest:
        contest = await self.get_contest_by_external_id(contest_external_id)
        if not contest:
            contest = Contest(
                external_id=contest_external_id,
                name=contest_data.get("name"),
            )
            self.session.add(contest)
            await self.session.commit()
            await self.session.refresh(contest)
        return contest


