from fastapi import Depends, HTTPException, status

from .problem_state_repository import ProblemStateRepository
from .proxy_manager import ProxyManager
from app.db.enums import ProblemStatusEnum
from app.db.models import ProblemState
from app.schemas import ProblemStateSchema


class ProblemStateManager:
    def __init__(
        self,
        proxy_manager: ProxyManager = Depends(ProxyManager),
        problem_state_repository: ProblemStateRepository = Depends(ProblemStateRepository),
    ):
        self.proxy_manager = proxy_manager
        self.problem_state_repository = problem_state_repository

    async def init_problem_states(self, contest_external_id, training_session_id):
        if await self.problem_state_repository.is_problem_states_exist(training_session_id):
            return

        contest_problems = await self.proxy_manager.get_contest_problems(training_session_id)
        problem_state_list: list[ProblemState] = []
        for problem in contest_problems.get("problems", []):
            problem_state = ProblemState(
                training_session_id=training_session_id,
                problem_alias=problem.get("alias"),
            )
            problem_state_list.append(problem_state)

        await self.problem_state_repository.save_all(problem_state_list=problem_state_list)

    async def adjust_problem_state(self, training_session_id, response_content):
        problem_state = await self.problem_state_repository.get_problem(
            training_session_id=training_session_id, alias=response_content.get("problemAlias")
        )
        if problem_state is not None:
            if response_content.get("verdict") == "OK":
                problem_state.status = ProblemStatusEnum.PASSED
            else:
                if problem_state.status != ProblemStatusEnum.FAILED:
                    problem_state.status = ProblemStatusEnum.FAILED

            problem_state.attempts += 1
            await self.problem_state_repository.update_problem_state(problem_state)

    async def get_problem_by_alias(
        self, training_session_id: str, alias: str,
    ) -> ProblemStateSchema:
        problem = await self.problem_state_repository.get_problem(
            training_session_id=training_session_id, alias=alias
        )
        if problem is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND)
        # HACK: remove this piece of shit
        problem.problemAlias = problem.problem_alias
        return ProblemStateSchema.model_validate(problem)
