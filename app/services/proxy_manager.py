from fastapi import Depends, HTTPException

from .contest_api_manager import ContestApiManager


class ProxyManager:
    # TODO: separate to different managers by api groups
    def __init__(
        self,
        contest_api_manager: ContestApiManager = Depends(ContestApiManager),
    ):
        self.contest_api_manager = contest_api_manager

    async def get_my_standing(self, contest_id: int) -> dict:
        result, status_code = await self.contest_api_manager.get_my_standing(contest_id)

        if status_code == 200:
            return result
        else:
            raise HTTPException(status_code=status_code)
