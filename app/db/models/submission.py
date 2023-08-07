from sqlalchemy import TEXT, UUID, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseTable
from .contest_training import ContestTraining
from .problem import Problem


class Submission(BaseTable):
    __tablename__ = "submissions"

    problem_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("problems.id"),
    )
    contest_training_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("contest_trainings.id"),
    )
    content: Mapped[str] = mapped_column(
        TEXT,
    )

    problem: Mapped[Problem] = relationship(backref="submissions")
    contest_training: Mapped[ContestTraining] = relationship(backref="submissions")
