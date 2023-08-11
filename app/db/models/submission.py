from sqlalchemy import TEXT, UUID, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseTable
from .training_session import TrainingSession


class Submission(BaseTable):
    __tablename__ = "submissions"

    problem_alias: Mapped[str] = mapped_column(
        String(255),
    )
    training_session_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("training_sessions.id"),
    )
    content: Mapped[str] = mapped_column(
        TEXT,
    )

    training_session: Mapped[TrainingSession] = relationship(backref="submissions", lazy="joined")
