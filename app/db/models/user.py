from .base import BaseTable

from sqlalchemy.dialects.postgresql import VARCHAR
from sqlalchemy.orm import Mapped, mapped_column


class User(BaseTable):
    __tablename__ = "users"

    external_id: Mapped[str] = mapped_column(
        VARCHAR,
        unique=True,
        doc="Unique external index of element",
    )
    login: Mapped[str] = mapped_column(
        VARCHAR,
        unique=True,
        doc="User's unique username"
    )
    first_name: Mapped[str] = mapped_column(
        VARCHAR,
        doc="User's first name",
        nullable=True,
    )
    last_name: Mapped[str] = mapped_column(
        VARCHAR,
        doc="User's last name",
        nullable=True,
    )
