from sqlalchemy import TEXT, UUID, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid import UUID as _UUID

from .base import BaseTable
from .training_session import TrainingSession
from .user import User


class Comment(BaseTable):
    __tablename__ = "comments"

    user_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
    )
    problem_alias: Mapped[str] = mapped_column(
        String(255),
    )
    training_session_id: Mapped[_UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("training_sessions.id"),
    )
    content: Mapped[str] = mapped_column(
        TEXT,
    )

    user: Mapped[User] = relationship(backref="comments", lazy="joined")
    training_session: Mapped[TrainingSession] = relationship(backref="comments", lazy="joined")
