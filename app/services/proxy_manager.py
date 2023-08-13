from fastapi import Depends, HTTPException, UploadFile

from .contest_api_manager import ContestApiManager
from .problem_state_repository import ProblemStateRepository


class ProxyManager:
    # TODO: separate to different managers by api groups
    def __init__(
        self,
        contest_api_manager: ContestApiManager = Depends(ContestApiManager),
        problem_state_repository: ProblemStateRepository = Depends(ProblemStateRepository),
    ):
        self.contest_api_manager = contest_api_manager
        self.problem_state_repository = problem_state_repository

    async def get_contest(self, contest_id: int) -> dict:
        result, status_code = await self.contest_api_manager.get_contest(contest_id)

        if status_code == 200:
            return result
        else:
            raise HTTPException(status_code=status_code)

    async def get_my_standing(self, contest_id: int) -> dict:
        result, status_code = await self.contest_api_manager.get_my_standing(contest_id)

        if status_code == 200:
            return result
        else:
            raise HTTPException(status_code=status_code)

    async def get_contest_problems(self, contest_id: int, training_session_id: str) -> dict:
        result, status_code = await self.contest_api_manager.get_contest_problems(contest_id)

        if status_code == 200:
            for problem in result.get("problems", []):
                problem_state = await self.problem_state_repository.get_problem(
                    training_session_id=training_session_id,
                    alias=problem.get("alias"),
                )
                if problem_state is not None:
                    problem["status"] = problem_state.status

            return result
        else:
            raise HTTPException(status_code=status_code)

    async def get_problem_statement(self, contest_id: int, alias: str) -> bytes:
        result, status_code = await self.contest_api_manager.get_problem_statement(
            contest_id, alias
        )

        if status_code == 200:
            return result
        else:
            raise HTTPException(status_code=status_code)

    async def submit_solution(
        self,
        contest_id: int,
        problem: str,
        compiler: str,
        file: UploadFile,
    ) -> dict:
        result, status_code = await self.contest_api_manager.submit_solution(
            contest_id, problem, compiler, file
        )
        if status_code == 200:
            return result
        else:
            raise HTTPException(status_code=status_code)

    async def get_submission_short(self, contest_id: int, submission_id: int) -> dict:
        result, status_code = await self.contest_api_manager.get_submission_short(
            contest_id, submission_id
        )
        if status_code == 200:
            return result
        else:
            raise HTTPException(status_code=status_code)

    async def get_submission_full(self, contest_id: int, submission_id: int) -> dict:
        result, status_code = await self.contest_api_manager.get_submission_full(
            contest_id, submission_id
        )
        if status_code == 200:
            return result
        else:
            raise HTTPException(status_code=status_code)

    async def get_submissions(self, contest_id: int) -> dict:
        result, status_code = await self.contest_api_manager.get_submissions(contest_id)
        if status_code == 200:
            return result
        else:
            raise HTTPException(status_code=status_code)

    async def get_me(self) -> dict:
        result, status_code = await self.contest_api_manager.get_me()
        if status_code == 200:
            return result
        else:
            raise HTTPException(status_code=status_code)
