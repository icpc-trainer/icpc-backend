from sqlalchemy import TEXT, UUID, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseTable
from .contest_training import ContestTraining
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
    contest_training_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("contest_trainings.id")
    )
    content: Mapped[str] = mapped_column(
        TEXT,
    )

    user: Mapped[User] = relationship(backref="comments")
    problem: Mapped[Problem] = relationship(backref="comments")
    contest_training: Mapped[ContestTraining] = relationship(backref="comments")
