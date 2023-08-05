from .base import BaseTable
from app.db.enums import TrainingStatusEnum

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID, ENUM
from sqlalchemy.orm import Mapped, mapped_column


class ContestTraining(BaseTable):
    __tablename__ = "contest_trainings"

    contest_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("contests.id"),
    )
    team_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("teams.id"),
    )
    status: Mapped[TrainingStatusEnum] = mapped_column(
        ENUM(TrainingStatusEnum),
        default=TrainingStatusEnum.IN_PROCESS,
    )
