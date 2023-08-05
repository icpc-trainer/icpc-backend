from .base import BaseTable

from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy.dialects.postgresql import VARCHAR
from sqlalchemy.orm import Mapped, mapped_column


class Team(BaseTable):
    __tablename__ = "teams"

    external_id: Mapped[str] = mapped_column(
        VARCHAR,
        unique=True,
        doc="Unique external index of element",
    )
    name: Mapped[str] = mapped_column(
        VARCHAR,
        doc="Team name"
    )


user_team = Table(
    "user_teams",
    BaseTable.metadata,
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("team_id", ForeignKey("teams.id"), primary_key=True),
)