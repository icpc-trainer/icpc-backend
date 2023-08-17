from fastapi import APIRouter, Depends, status
from fastapi.responses import StreamingResponse

from app.schemas import ProblemStateSchema
from app.services import ProblemStateManager, ProxyManager


router = APIRouter(
    prefix="/contests",
    tags=["problems"],
)


@router.get(
    "/{training_session_id}/problems",
    status_code=status.HTTP_200_OK,
)
async def contest_problems(
    training_session_id: str,
    proxy_manager: ProxyManager = Depends(ProxyManager),
) -> dict:
    problems = await proxy_manager.get_contest_problems(training_session_id=training_session_id)
    return problems


@router.get(
    "/{training_session_id}/problems/{alias}",
    status_code=status.HTTP_200_OK,
)
async def get_contest_problem_by_alias(
    training_session_id: str,
    alias: str,
    problem_state_manager: ProblemStateManager = Depends(ProblemStateManager),
) -> ProblemStateSchema:
    problem = await problem_state_manager.get_problem_by_alias(
        training_session_id=training_session_id,
        alias=alias,
    )
    return problem


@router.get(
    "/{training_session_id}/problems/{alias}/statement",
    status_code=status.HTTP_200_OK,
)
async def problem_statement(
    training_session_id: str,
    alias: str,
    proxy_manager: ProxyManager = Depends(ProxyManager),
) -> StreamingResponse:
    result = await proxy_manager.get_problem_statement(
        training_session_id,
        alias
    )
    return StreamingResponse(iter([result]), media_type="application/octet-stream")
