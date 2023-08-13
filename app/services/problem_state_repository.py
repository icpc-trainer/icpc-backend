from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, exists

from app.db.connection import get_session
from app.db.models import ProblemState


class ProblemStateRepository:
    def __init__(self, session: AsyncSession = Depends(get_session)):
        self.session = session

    async def save_all(self, problem_state_list: list[ProblemState]) -> None:
        self.session.add_all(problem_state_list)
        await self.session.commit()

    async def update_problem_state(self, problem_state: ProblemState) -> None:
        self.session.add(problem_state)
        await self.session.commit()

    async def is_problem_states_exist(self, training_session_id: str) -> bool:
        exists_query = await self.session.execute(
            select(exists().where(ProblemState.training_session_id == training_session_id))
        )
        exists_problem = exists_query.scalar()
        if exists_problem is None:
            return False
        return exists_problem

    async def get_problem(self, training_session_id: str, alias: str) -> ProblemState | None:
        query = select(ProblemState).where(
            ProblemState.training_session_id == training_session_id,
            ProblemState.problem_alias == alias,
        )
        return await self.session.scalar(query)
