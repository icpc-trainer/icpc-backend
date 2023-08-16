from fastapi import Depends, HTTPException, UploadFile

from .contest_api_manager import ContestApiManager
from .problem_state_repository import ProblemStateRepository
from .training_session_repository import TrainingSessionRepository
from .redis_storage_manager import RedisStorageManager



class ProxyManager:
    # TODO: separate to different managers by api groups
    def __init__(
        self,
        contest_api_manager: ContestApiManager = Depends(ContestApiManager),
        problem_state_repository: ProblemStateRepository = Depends(ProblemStateRepository),
        training_session_repository: TrainingSessionRepository = Depends(TrainingSessionRepository),
        redis_storage_manager: RedisStorageManager = Depends(),
    ):
        self.contest_api_manager = contest_api_manager
        self.problem_state_repository = problem_state_repository
        self.training_session_repository = training_session_repository
        self.redis_storage_manager = redis_storage_manager

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

    async def get_contest_problems(self, training_session_id: str) -> dict:
        training_session = await self.training_session_repository.get_training_session_by_id(
            training_session_id
        )
        contest_id = int(training_session.contest.external_id)

        result, status_code = await self.contest_api_manager.get_contest_problems(contest_id)

        if status_code == 200:
            for problem in result.get("problems", []):
                problem_state = await self.problem_state_repository.get_problem(
                    training_session_id=training_session_id,
                    alias=problem.get("alias"),
                )
                if problem_state is not None:
                    problem["status"] = problem_state.status
                    problem["attempts"] = problem_state.attempts

                user = self.redis_storage_manager.assigments.get(
                    training_session_id=training_session_id,
                    alias=problem.get("alias"),
                )

                problem["assignedUser"] = user

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

    async def register_for_contest(self, contest_id: int, team_id: int) -> dict:
        result, status_code = await self.contest_api_manager.register_for_contest(contest_id, team_id)
        if status_code == 201 or status_code == 200 or status_code == 409:
            return result
        else:
            raise HTTPException(status_code=status_code)

    async def start_the_contest(self, contest_id: int) -> dict:
        result, status_code = await self.contest_api_manager.start_the_contest(contest_id)
        if status_code == 201 or status_code == 200 or status_code == 409:
            return result
        else:
            raise HTTPException(status_code=status_code)

    async def get_user_teams(self) -> dict:
        result, status_code = await self.contest_api_manager.get_user_teams()
        if status_code == 200:
            return result
        else:
            raise HTTPException(status_code=status_code)