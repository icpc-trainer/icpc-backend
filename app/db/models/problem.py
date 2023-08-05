from .base import BaseTable

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID, VARCHAR
from sqlalchemy.orm import Mapped, mapped_column


class Problem(BaseTable):
    __tablename__ = "problems"

    external_id: Mapped[str] = mapped_column(
        VARCHAR,
        unique=True,
        doc="Unique external index of element",
    )
    contest_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("contests.id"),
    )
    content: Mapped[str] = mapped_column(
        VARCHAR,
        doc="Problem description"
    )


