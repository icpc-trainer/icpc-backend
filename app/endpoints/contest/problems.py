from fastapi import APIRouter, Depends, Form
from fastapi.responses import StreamingResponse
from starlette import status

from app.services import ProxyManager, ProblemRepository, ContestRepository


router = APIRouter(
    prefix="/contests",
    tags=["problems"],
)


@router.get(
    "/{contest_id}/problems",
    status_code=status.HTTP_200_OK,
)
async def contest_problems(
    contest_id: int,
    proxy_manager: ProxyManager = Depends(ProxyManager),
    problem_repository: ProblemRepository = Depends(),
    contest_repository: ContestRepository = Depends(),
) -> dict:
    problems = await proxy_manager.get_contest_problems(contest_id)
    contest = await contest_repository.get_contest_by_external_id(str(contest_id))
    for problem in problems.get("problems"):
        await problem_repository.create_if_not_exists(
            contest.id, problem
        )
    return problems


@router.get(
    "/{contest_id}/problems/{alias}/statement",
    status_code=status.HTTP_200_OK,
)
async def problem_statement(
    contest_id: int,
    alias: str,
    proxy_manager: ProxyManager = Depends(ProxyManager),
) -> dict:
    result = await proxy_manager.get_problem_statement(contest_id, alias)
    return StreamingResponse(iter([result]), media_type="application/octet-stream")