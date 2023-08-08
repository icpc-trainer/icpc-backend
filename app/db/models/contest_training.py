from sqlalchemy import UUID, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseTable
from .contest import Contest
from .team import Team
from app.db.enums import TrainingStatusEnum


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
        Enum(TrainingStatusEnum),
        default=TrainingStatusEnum.IN_PROCESS,
    )

    contest: Mapped[Contest] = relationship(backref="contest_trainings", lazy="joined")
    team: Mapped[Team] = relationship(backref="contest_trainings", lazy="joined")
