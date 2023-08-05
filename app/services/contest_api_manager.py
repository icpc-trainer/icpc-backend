from app.config import settings


class ContestApiManager:
    @staticmethod
    def get_url() -> str:
        return settings.CONTEST_API_URL

    def __init__(self, authorization: str):
        self.authorization = authorization

    async def get_teams(self):
        pass

    async def call_(self):
        pass
