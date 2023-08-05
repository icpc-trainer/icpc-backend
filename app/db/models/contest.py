from .base import BaseTable

from sqlalchemy import String 
from sqlalchemy.orm import Mapped, mapped_column


class Contest(BaseTable):
    __tablename__ = "contests"

    external_id: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        doc="Unique external index of element",
    )
    name: Mapped[str] = mapped_column(
        String(255),
        doc="Contest name"
    )



