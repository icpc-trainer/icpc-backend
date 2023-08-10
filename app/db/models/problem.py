from sqlalchemy import TEXT, UUID, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseTable
from .contest import Contest


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
    alias: Mapped[str] = mapped_column(
        String(1),
    )

    contest: Mapped[Contest] = relationship(backref="problems", lazy="joined")
