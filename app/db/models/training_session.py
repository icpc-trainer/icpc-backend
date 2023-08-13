from uuid import UUID as _UUID

from sqlalchemy import UUID, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseTable
from .contest import Contest
from .team import Team
from app.db.enums import TrainingStatusEnum


class TrainingSession(BaseTable):
    __tablename__ = "training_sessions"

    contest_id: Mapped[_UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("contests.id"),
    )
    team_id: Mapped[_UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("teams.id"),
    )
    status: Mapped[TrainingStatusEnum] = mapped_column(
        Enum(TrainingStatusEnum),
        default=TrainingStatusEnum.IN_PROCESS,
    )

    contest: Mapped[Contest] = relationship(backref="training_sessions", lazy="joined")
    team: Mapped[Team] = relationship(backref="training_sessions", lazy="joined")
