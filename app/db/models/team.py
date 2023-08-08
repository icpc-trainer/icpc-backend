from sqlalchemy import Column, ForeignKey, String, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseTable
from .user import User


user_team = Table(
    "user_teams",
    BaseTable.metadata,
    Column("user_id", ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
    Column("team_id", ForeignKey("teams.id", ondelete="CASCADE"), primary_key=True),
)


class Team(BaseTable):
    __tablename__ = "teams"

    external_id: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        doc="Unique external index of element",
    )
    name: Mapped[str] = mapped_column(
        String(255),
        doc="Team name",
    )

    users: Mapped[list[User]] = relationship(secondary=user_team, backref="teams", lazy="joined")
