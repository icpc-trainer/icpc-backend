from .base import BaseTable

from sqlalchemy import ForeignKey, UUID, TEXT
from sqlalchemy.orm import Mapped, mapped_column


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
    status: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("contest_trainings.id")
    )
    content: Mapped[str] = mapped_column(
        TEXT,
    )

