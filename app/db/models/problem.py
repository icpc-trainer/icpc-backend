from .base import BaseTable

from sqlalchemy import ForeignKey, UUID, TEXT, String
from sqlalchemy.orm import Mapped, mapped_column


class Problem(BaseTable):
    __tablename__ = "problems"

    external_id: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        doc="Unique external index of element",
    )
    contest_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("contests.id"),
    )
    content: Mapped[str] = mapped_column(
        TEXT,
        doc="Problem description"
    )


