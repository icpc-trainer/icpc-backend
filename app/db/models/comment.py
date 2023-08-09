from sqlalchemy import TEXT, UUID, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseTable
from .training_session import TrainingSession
from .problem import Problem
from .user import User


class Comment(BaseTable):
    __tablename__ = "comments"

    user_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
    )
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

    user: Mapped[User] = relationship(backref="comments", lazy="joined")
    problem: Mapped[Problem] = relationship(backref="comments", lazy="joined")
    training_session: Mapped[TrainingSession] = relationship(backref="comments", lazy="joined")
