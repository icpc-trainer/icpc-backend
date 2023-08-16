from fastapi import Depends

from .team_repository import TeamRepository
from .proxy_manager import ProxyManager
from app.db.models import Team


class TeamManager:
    def __init__(
        self,
        proxy_manager: ProxyManager = Depends(ProxyManager),
        team_repository: TeamRepository = Depends(TeamRepository),
    ):
        self.proxy_manager = proxy_manager
        self.team_repository = team_repository

    async def init_teams(self, teams):
        team_list: list[Team] = []

        for team in teams:
            if await self.team_repository.is_team_exist(str(team['id'])):
                continue
            team_list.append(Team(external_id=team['id'], name= team['name']))

        await self.team_repository.save_all(team_list)
