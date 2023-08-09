from uuid import UUID

from fastapi import Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.connection import get_session
from app.db.enums import TrainingStatusEnum
from app.db.models import Contest, TrainingSession, Team


class TrainingSessionRepository:
    def __init__(self, session: AsyncSession = Depends(get_session)):
        self.session = session

    async def get_training_session(
        self,
        contest_external_id: str,
        team_external_id: str,
    ) -> TrainingSession:
        # Запросы на получение контеста и команды
        contest_query = await self.session.execute(
            select(Contest).filter_by(external_id=contest_external_id)
        )
        contest = contest_query.scalar_one_or_none()
        if contest is None:
            raise HTTPException(
                status_code=404, detail=f"Контест с id {contest_external_id} не найден"
            )

        team_query = await self.session.execute(
            select(Team).filter_by(external_id=team_external_id)
        )
        team = team_query.scalar_one_or_none()
        if team is None:
            raise HTTPException(
                status_code=404, detail=f"Команда с id {team_external_id} не найдена"
            )

        training_session_query = await self.session.execute(
            select(TrainingSession).filter_by(contest_id=contest.id, team_id=team.id)
        )

        training_session = training_session_query.scalar_one_or_none()

        if training_session is None:
            training_session = TrainingSession(contest_id=contest.id, team_id=team.id)
            self.session.add(training_session)
            await self.session.commit()
            await self.session.refresh(training_session)

        return training_session

    async def complete_training_session(
        self,
        training_session_id: UUID,
    ) -> TrainingSession:
        training_session_query = await self.session.execute(
            select(TrainingSession).where(TrainingSession.id == training_session_id)
        )

        training_session = training_session_query.scalar_one_or_none()

        if training_session is None:
            raise HTTPException(
                status_code=404, detail=f"Тренировка с id {training_session_id} не найдена"
            )

        training_session.status = TrainingStatusEnum.FINISHED
        self.session.add(training_session)
        await self.session.commit()
        await self.session.refresh(training_session)

        return training_session
