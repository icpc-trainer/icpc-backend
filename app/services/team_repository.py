from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, exists

from app.db.connection import get_session
from app.db.models import Team


class TeamRepository:
    def __init__(self, session: AsyncSession = Depends(get_session)):
        self.session = session

    async def save_all(self, team_list: list[Team]) -> None:
        self.session.add_all(team_list)
        await self.session.commit()

    async def is_team_exist(self, team_external_id: str) -> bool:
        exists_query = await self.session.execute(
            select(exists().where(Team.external_id == team_external_id))
        )
        exists_team = exists_query.scalar()
        if exists_team is None:
            return False
        return exists_team
