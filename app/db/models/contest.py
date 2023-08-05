from .base import BaseTable

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID, VARCHAR
from sqlalchemy.orm import Mapped, mapped_column


class Contest(BaseTable):
    __tablename__ = "contests"

    external_id: Mapped[str] = mapped_column(
        VARCHAR,
        unique=True,
        doc="Unique external index of element",
    )
    name: Mapped[str] = mapped_column(
        VARCHAR,
        doc="Contest name"
    )



