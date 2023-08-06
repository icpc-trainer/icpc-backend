from .base import BaseTable

from sqlalchemy import ForeignKey, UUID, TEXT
from sqlalchemy.orm import Mapped, mapped_column


class Submission(BaseTable):
    __tablename__ = "submissions"

    problem_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("problems.id"),
    )
    contest_training_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("contests.id"),
    )
    content: Mapped[str] = mapped_column(
        TEXT,
    )



