from fastapi import APIRouter, Depends, File, Form, UploadFile, Security, BackgroundTasks
from fastapi.security.api_key import APIKeyHeader
from starlette import status

from app.services import ProxyManager, TrainingSessionRepository, ProblemStateManager
from app.background_tasks import get_submission_verdict
from app.services import training_manager
from app.db.enums import MessageTypeEnum
from app.utils import WebSocketMessage


router = APIRouter(
    prefix="/training-sessions",
    tags=["submission"],
)


@router.post(
    "/{training_session_id}/submissions",
    status_code=status.HTTP_200_OK,
)
async def submit_solution(
    background_tasks: BackgroundTasks,
    training_session_id: str,
    file: UploadFile = File(...),
    compiler: str = Form(...),
    problem: str = Form(...),
    proxy_manager: ProxyManager = Depends(ProxyManager),
    problem_state_manager: ProblemStateManager = Depends(ProblemStateManager),
    oauth_token: str = Security(APIKeyHeader(name="Authorization")),
    training_session_repository: TrainingSessionRepository = Depends(),
) -> dict:
    # получение contest_id через training session
    training_session = await training_session_repository.get_training_session_by_id(
        training_session_id
    )
    contest_id = training_session.contest.external_id

    # отправка ответа на задачу в контест апи и получение runId
    result = await proxy_manager.submit_solution(
        int(contest_id),
        problem,
        compiler,
        file,
    )

    # создание фоновой задачи на мониторинг вердикта отправки
    submission_id = result.get("runId")
    background_tasks.add_task(
        get_submission_verdict,
        problem_state_manager,
        oauth_token,
        contest_id,
        submission_id,
        training_session_id,
    )
    return result


@router.get(
    "/{training_session_id}/submissions/{submission_id}",
    status_code=status.HTTP_200_OK,
)
async def get_submission_short(
    training_session_id: str,
    submission_id: int,
    proxy_manager: ProxyManager = Depends(ProxyManager),
    training_session_repository: TrainingSessionRepository = Depends(),
) -> dict:
    # получение contest_id через training session
    training_session = await training_session_repository.get_training_session_by_id(
        training_session_id
    )
    contest_id = training_session.contest.external_id

    result = await proxy_manager.get_submission_short(contest_id, submission_id)
    return result


@router.get(
    "/{training_session_id}/submissions/{submission_id}/full",
    status_code=status.HTTP_200_OK,
)
async def get_submission_full(
    training_session_id: str,
    submission_id: int,
    proxy_manager: ProxyManager = Depends(ProxyManager),
    training_session_repository: TrainingSessionRepository = Depends(),
) -> dict:
    # получение contest_id через training session
    training_session = await training_session_repository.get_training_session_by_id(
        training_session_id
    )
    contest_id = training_session.contest.external_id

    result = await proxy_manager.get_submission_full(contest_id, submission_id)
    return result


@router.get(
    "/{training_session_id}/submissions/",
    status_code=status.HTTP_200_OK,
)
async def get_submissions_all(
    training_session_id: str,
    proxy_manager: ProxyManager = Depends(ProxyManager),
    training_session_repository: TrainingSessionRepository = Depends(),
) -> dict:
    # получение contest_id через training session
    training_session = await training_session_repository.get_training_session_by_id(
        training_session_id
    )
    contest_id = training_session.contest.external_id

    result = await proxy_manager.get_submissions(contest_id)
    return result


@router.get(
    "/{training_session_id}/submissions/problem/{problem_alias}",
    status_code=status.HTTP_200_OK,
)
async def get_submissions_by_problem(
    training_session_id: str,
    problem_alias: str,
    proxy_manager: ProxyManager = Depends(ProxyManager),
    training_session_repository: TrainingSessionRepository = Depends(),
) -> dict:
    # получение contest_id через training session
    training_session = await training_session_repository.get_training_session_by_id(
        training_session_id
    )
    contest_id = training_session.contest.external_id
    result = await proxy_manager.get_submissions(contest_id)
    response = []
    for submission in result.get("submissions"):
        if submission.get("problemAlias") == problem_alias:
            response.append(submission)

    return {
        "count": len(response),
        "submissions": response,
    }


