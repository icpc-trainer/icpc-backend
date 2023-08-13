from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from starlette import status

from app.services import ProxyManager


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
    "/{contest_id}/problems/{alias}/statement",
    status_code=status.HTTP_200_OK,
)
async def problem_statement(
    contest_id: int,
    alias: str,
    proxy_manager: ProxyManager = Depends(ProxyManager),
) -> StreamingResponse:
    result = await proxy_manager.get_problem_statement(contest_id, alias)
    return StreamingResponse(iter([result]), media_type="application/octet-stream")
