from uuid import UUID as _UUID

from sqlalchemy import UUID, Enum, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseTable
from .training_session import TrainingSession
from app.db.enums import ProblemStatusEnum


class ProblemState(BaseTable):
    __tablename__ = "problem_states"
    __table_args__ = (
        UniqueConstraint("training_session_id", "problem_alias"),
    )

    training_session_id: Mapped[_UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("training_sessions.id"),
    )
    problem_alias: Mapped[str] = mapped_column(
        String(255),
    )
    status: Mapped[ProblemStatusEnum] = mapped_column(
        Enum(ProblemStatusEnum),
        default=ProblemStatusEnum.NOT_SUBMITTED,
    )
    attempts: Mapped[int] = mapped_column(
        default=0,
    )

    training_session: Mapped[TrainingSession] = relationship(
        backref="problem_states", lazy="joined"
    )
