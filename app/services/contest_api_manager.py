import httpx
from fastapi import Security, UploadFile, HTTPException, status
from fastapi.security.api_key import APIKeyHeader

from app.config import settings


# from sqlalchemy.ext.asyncio import AsyncSession
# from app.db.connection import get_session


class ContestApiManager:
    # TODO: separate to different managers by api groups
    @staticmethod
    def get_url() -> str:
        return settings.CONTEST_API_URL

    def __init__(self, authorization: str = Security(APIKeyHeader(name="Authorization"))):
        self.authorization = authorization

    async def get_contest(self, contest_id: int) -> tuple[dict, int]:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                url=f"{self.get_url()}/contests/{contest_id}",
                headers={"Authorization": self.authorization},
            )
            status_code = response.status_code
            if status_code == 200:
                return response.json(), response.status_code
            else:
                return {}, response.status_code

    async def get_my_standing(self, contest_id: int) -> tuple[dict, int]:
        # TODO: add optional parametrs
        async with httpx.AsyncClient() as client:
            response = await client.get(
                url=f"{self.get_url()}/contests/{contest_id}/standings/my",
                headers={"Authorization": self.authorization},
            )
            status_code = response.status_code
            if status_code == 200:
                return response.json(), response.status_code
            else:
                return {}, response.status_code

    async def get_contest_problems(self, contest_id: int) -> tuple[dict, int]:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                url=f"{self.get_url()}/contests/{contest_id}/problems",
                headers={"Authorization": self.authorization},
            )
            status_code = response.status_code
            if status_code == 200:
                return response.json(), response.status_code
            else:
                return {}, response.status_code

    async def get_problem_statement(self, contest_id: int, alias: str) -> tuple[bytes, int]:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                url=f"{self.get_url()}/contests/{contest_id}/problems/{alias}/statement",
                headers={"Authorization": self.authorization},
            )
            status_code = response.status_code
            if status_code == 200:
                return response.content, response.status_code
            else:
                return b"", response.status_code

    async def submit_solution(
        self,
        contest_id: int,
        problem: str,
        compiler: str,
        file: UploadFile,
    ) -> tuple[dict, int]:
        async with httpx.AsyncClient() as client:
            body = {
                "compiler": compiler,
                "problem": problem,
            }
            response = await client.post(
                url=f"{self.get_url()}/contests/{contest_id}/submissions",
                headers={"Authorization": self.authorization},
                data=body,
                files={"file": (file.filename, file.file, file.content_type)},
            )
            status_code = response.status_code
            if status_code == 200:
                return response.json(), response.status_code
            else:
                return {"message": response.content.decode()}, response.status_code

    async def get_submission_short(self, contest_id: int, submission_id: int) -> tuple[dict, int]:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                url=f"{self.get_url()}/contests/{contest_id}/submissions/{submission_id}",
                headers={"Authorization": self.authorization},
            )
            status_code = response.status_code
            if status_code == 200:
                return response.json(), response.status_code
            else:
                return {}, response.status_code

    async def get_submission_full(self, contest_id: int, submission_id: int) -> tuple[dict, int]:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                url=f"{self.get_url()}/contests/{contest_id}/submissions/{submission_id}/full",
                headers={"Authorization": self.authorization},
            )
            status_code = response.status_code
            if status_code == 200:
                return response.json(), response.status_code
            else:
                return {}, response.status_code

    async def get_submissions(self, contest_id: int) -> tuple[dict, int]:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                url=f"{self.get_url()}/contests/{contest_id}/submissions/",
                headers={"Authorization": self.authorization},
            )
            status_code = response.status_code
            if status_code == 200:
                return response.json(), response.status_code
            else:
                return {}, response.status_code

    async def get_me(self) -> tuple[dict, int]:
        async with httpx.AsyncClient() as client:
            params = {
                "format": "json",
                "oauth_token": self.authorization.split()[1],
            }
            response = await client.get(
                url=f"{settings.AUTH_API_URL}/info",
                params=params,
                headers={"Authorization": self.authorization},
            )
            status_code = response.status_code
            if status_code == 200:
                return response.json(), response.status_code
            else:
                return {}, response.status_code

    async def register_for_contest(self, contest_id: int, team_id: int) -> tuple[dict, int]:
        try:
            async with httpx.AsyncClient() as client:
                body = {
                    "contestId": contest_id,
                    "teamId": team_id,
                }
                response = await client.post(
                    url=f"{self.get_url()}/contests/{contest_id}/participants",
                    headers={"Authorization": self.authorization},
                    data=body,
                )
                status_code = response.status_code
                if status_code == 201 or status_code == 200:
                    return {"message": response.content.decode()}, response.status_code
                else:
                    return {"message": response.content.decode()}, response.status_code
        except httpx.TimeoutException:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Connection to remote server timed out"
            )

    async def start_the_contest(self, contest_id: int) -> tuple[dict, int]:
        try:
            async with httpx.AsyncClient(timeout=20) as client:
                body = {
                    "contestId": contest_id,
                }
                response = await client.put(
                    url=f"{self.get_url()}/contests/{contest_id}/participation",
                    headers={"Authorization": self.authorization},
                    data=body,
                )
                status_code = response.status_code
                if status_code == 200:
                    return {"message": response.content.decode()}, response.status_code
                else:
                    return {"message": response.content.decode()}, response.status_code
        except httpx.TimeoutException:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Connection to remote server timed out"
            )

    async def get_user_teams(self) -> tuple[dict, int]:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                url=f"{self.get_url()}/teams",
                headers={"Authorization": self.authorization},
            )
            status_code = response.status_code
            if status_code == 200:
                return response.json(), response.status_code
            else:
                return {}, response.status_code

    async def get_contest_standings(self, contest_id: int) -> tuple[dict, int]:
        # TODO: add optional parametrs
        async with httpx.AsyncClient() as client:
            response = await client.get(
                url=f"{self.get_url()}/contests/{contest_id}/standings",
                headers={"Authorization": self.authorization},
            )
            status_code = response.status_code
            if status_code == 200:
                return response.json(), response.status_code
            else:
                return {}, response.status_code

    async def get_information_about_your_participation(self, contest_id: int) -> tuple[dict, int]:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                url=f"{self.get_url()}/contests/{contest_id}/participation",
                headers={"Authorization": self.authorization},
            )
            status_code = response.status_code
            if status_code == 200:
                return response.json(), response.status_code
            else:
                return {}, response.status_code


if __name__ == "__main__":
    # TODO: Move to unit tests
    manager = ContestApiManager(
        authorization="OAuth y0_AgAAAABpKy-JAApD0QAAAADpWj8IYWEY5IXGQpW_y-_teZB4tQ-meUc"
    )

    async def main():
        response = await manager.get_my_standing(contest_id=50952)
        # response = await manager.register_for_contest(contest_id=51397, team_id=6022)
        response = await manager.start_the_contest(contest_id=51397)
        # response = await manager.get_problems(contest_id=50952)
        print(response)

    import asyncio

    asyncio.run(main())
