from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.connection import get_session
from app.db.models import ContestTraining, Contest, Team
from app.db.enums import TrainingStatusEnum


class ContestTrainingRepository:
    def __init__(self, session: AsyncSession = Depends(get_session)):
        self.session = session

    async def get_contest_training(
        self,
        contest_external_id: str,
        team_external_id: str,
    ) -> ContestTraining:
        # Запросы на получение контеста и команды
        contest_query = await self.session.execute(
            select(Contest).filter_by(external_id=contest_external_id)
        )

        team_query = await self.session.execute(
            select(Team).filter_by(external_id=team_external_id)
        )

        contest = contest_query.scalar_one_or_none()
        team = team_query.scalar_one_or_none()

        if contest is None:
            raise HTTPException(status_code=404, detail=f"Контест с id {contest_external_id} не найден")

        if team is None:
            raise HTTPException(status_code=404, detail=f"Команда с id {team_external_id} не найдена")

        contest_training_query = await self.session.execute(
            select(ContestTraining).filter_by(contest_id=contest.id, team_id=team.id)
        )

        contest_training = contest_training_query.scalar_one_or_none()

        if contest_training is None:
            contest_training = ContestTraining(contest_id=contest.id, team_id=team.id)
            self.session.add(contest_training)
            await self.session.commit()
            await self.session.refresh(contest_training)

        return contest_training

    async def complete_contest_training(
        self,
        contest_training_id: str,
    ) -> ContestTraining:
        contest_training_query = await self.session.execute(
            select(ContestTraining).where(ContestTraining.id==contest_training_id)
        )

        contest_training = contest_training_query.scalar_one_or_none()

        if contest_training is None:
            raise HTTPException(status_code=404, detail=f"Тренировка с id {contest_training_id} не найдена")

        contest_training.status = TrainingStatusEnum.FINISHED
        self.session.add(contest_training)
        await self.session.commit()
        await self.session.refresh(contest_training)

        return contest_training
