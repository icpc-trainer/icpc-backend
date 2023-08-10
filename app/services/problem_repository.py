from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.connection import get_session
from app.db.models import Problem


class ProblemRepository:
    def __init__(self, session: AsyncSession = Depends(get_session)):
        self.session = session

    async def get_problem_by_contest_id_and_alias(
        self,
        contest_id: int,
        problem_alias: str,
    ) -> Problem:
        query = select(Problem).where(
            Problem.contest_id==contest_id,
            Problem.alias==problem_alias,
        )
        return await self.session.scalar(query)
