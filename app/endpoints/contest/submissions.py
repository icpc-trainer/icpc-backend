from fastapi import APIRouter, UploadFile, Depends, File, Form
from starlette import status

from app.services import ProxyManager


router = APIRouter(
    prefix="/contests",
    tags=["standings"],
)


@router.post(
    "/{contest_id}/submissions",
    status_code=status.HTTP_200_OK,
)
async def submit_solution(
    contest_id: int,
    file: UploadFile = File(...),
    compiler: str = Form(...),
    problem: str = Form(...),
    proxy_manager: ProxyManager = Depends(ProxyManager),
) -> dict:
    result = await proxy_manager.submit_solution(
        contest_id,
        problem,
        compiler,
        file
    )
    return result
