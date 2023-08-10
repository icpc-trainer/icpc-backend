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
        contest_id: str,
        problem_alias: str,
    ) -> Problem:
        query = select(Problem).where(
            Problem.contest_id==contest_id,
            Problem.alias==problem_alias,
        )
        return await self.session.scalar(query)

    async def create_if_not_exists(
        self,
        contest_id: str,
        problem_data: dict,
    ) -> Problem:
        problem = await self.get_problem_by_contest_id_and_alias(
            contest_id, problem_data.get("alias"),
        )
        if not problem:
            problem = Problem(
                contest_id=contest_id,
                alias=problem_data.get("alias"),
            )
            self.session.add(problem)
            await self.session.commit()
            await self.session.refresh(problem)
        return problem
