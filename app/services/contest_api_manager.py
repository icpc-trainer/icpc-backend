import httpx

from app.config import settings


class ContestApiManager:
    @staticmethod
    def get_url() -> str:
        return settings.CONTEST_API_URL

    def __init__(self, authorization: str):
        self.authorization = authorization

    async def get_my_standing(self, contest_id: int) -> dict:
        # return [{"good": "good"}]
        async with httpx.AsyncClient() as client:
            response = await client.get(
                url=f"{self.get_url()}/contests/{contest_id}/standings/my",
                headers={"Authorization": self.authorization},
            )
            if response.status_code == 200:
                return response.json()
            else:
                raise ConnectionError  # NOTE: custom errors


if __name__ == "__main__":
    # TODO:
    manager = ContestApiManager(
        authorization="OAuth y0_AgAAAABpKy-JAApD0QAAAADpWj8IYWEY5IXGQpW_y-_teZB4tQ-meUc"
    )

    async def main():
        response = await manager.get_my_standing(contest_id=50952)
        print(response)

    import asyncio

    asyncio.run(main())
