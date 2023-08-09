from sqlalchemy import TEXT, UUID, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseTable
from .training_session import TrainingSession
from .problem import Problem


class Submission(BaseTable):
    __tablename__ = "submissions"

    problem_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("problems.id"),
    )
    training_session_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("training_sessions.id"),
    )
    content: Mapped[str] = mapped_column(
        TEXT,
    )

    problem: Mapped[Problem] = relationship(backref="submissions", lazy="joined")
    training_session: Mapped[TrainingSession] = relationship(backref="submissions", lazy="joined")
