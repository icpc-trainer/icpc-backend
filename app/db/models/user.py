from .base import BaseTable

from sqlalchemy import String 
from sqlalchemy.orm import Mapped, mapped_column


class User(BaseTable):
    __tablename__ = "users"

    external_id: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        doc="Unique external index of element",
    )
    login: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        doc="User's unique username"
    )
    first_name: Mapped[str] = mapped_column(
        String(255),
        doc="User's first name",
        nullable=True,
    )
    last_name: Mapped[str] = mapped_column(
        String(255),
        doc="User's last name",
        nullable=True,
    )
