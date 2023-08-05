from .base import BaseTable

from sqlalchemy import Table, Column, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column


class Team(BaseTable):
    __tablename__ = "teams"

    external_id: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        doc="Unique external index of element",
    )
    name: Mapped[str] = mapped_column(
        String(255),
        doc="Team name"
    )


user_team = Table(
    "user_teams",
    BaseTable.metadata,
    Column("user_id", ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
    Column("team_id", ForeignKey("teams.id", ondelete="CASCADE"), primary_key=True),
)