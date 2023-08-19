from uuid import UUID
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, Query, status, BackgroundTasks

from app.db.enums import MessageTypeEnum
from app.schemas import TrainingSessionSchema, TrainingSessionRequest
from app.services import (
    ProblemStateManager,
    TrainingSessionRepository,
    RedisStorageManager,
    ProxyManager,
    training_manager,
    lobby_manager,
)
from app.utils import WebSocketMessage
from app.background_tasks import training_session_finisher


router = APIRouter(
    prefix="/training-sessions",
    tags=["Training Sessions"],
)


@router.get(
    "",
    status_code=status.HTTP_200_OK,
)
async def get_training_session(
    contest_external_id: str = Query(alias="contest_id"),
    team_external_id: str = Query(alias="team_id"),
    training_session_repository: TrainingSessionRepository = Depends(),
) -> TrainingSessionSchema:
    training_session = await training_session_repository.get_training_session(
        contest_external_id,
        team_external_id,
    )

    return TrainingSessionSchema.model_validate(training_session)


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_503_SERVICE_UNAVAILABLE: {
            "description": "Connection to remote server timed out",
        },
    },
)
async def create_training_session(
    body: TrainingSessionRequest,
    background_tasks: BackgroundTasks,
    training_session_repository: TrainingSessionRepository = Depends(),
    problem_state_manager: ProblemStateManager = Depends(),
    proxy_manager: ProxyManager = Depends(ProxyManager),
) -> TrainingSessionSchema:
    # 1. РЕГИСТРАЦИЯ КОМАНДЫ
    await proxy_manager.register_for_contest(body.contest_id, body.team_id)

    # 2. СТАРТ ВИРТУАЛЬНОГО СОРЕВНОВАНИЯ
    await proxy_manager.start_the_contest(body.contest_id)

    # 3. ПОЛУЧЕНИЕ КОНТЕСТА
    training_session = await training_session_repository.create_training_session(
        contest_external_id=body.contest_id,
        team_external_id=body.team_id,
    )

    # 4. Инициализация состояний проблем
    await problem_state_manager.init_problem_states(
        contest_external_id=body.contest_id,
        training_session_id=training_session.id,
    )

    # 5. Уведомление всей команды о старте
    message = WebSocketMessage(
        type=MessageTypeEnum.TRAINING_STARTED,
        payload={
            "id": str(training_session.id),
            "status": training_session.status,
            "dtCreated": str(training_session.dt_created),
        },
    )

    await lobby_manager.broadcast(str(body.team_id), message.json())

    contest = await proxy_manager.get_contest(body.contest_id)
    background_tasks.add_task(
        training_session_finisher,
        timedelta(seconds=int(contest.get("duration"))),
        training_session.id,
        training_session_repository,
    )

    return TrainingSessionSchema.model_validate(training_session)


@router.get(
    "/{training_session_id}",
    status_code=status.HTTP_200_OK,
)
async def get_training_session_by_id(
    training_session_id: str,
    training_session_repository: TrainingSessionRepository = Depends(),
) -> TrainingSessionSchema:
    training_session = await training_session_repository.get_training_session_by_id(
        training_session_id,
    )

    return TrainingSessionSchema.model_validate(training_session)


@router.post(
    "/{training_session_id}/complete",
    status_code=status.HTTP_200_OK,
)
async def complete_training_session(
    training_session_id: UUID,
    training_session_repository: TrainingSessionRepository = Depends(),
) -> TrainingSessionSchema:
    training_session = await training_session_repository.complete_training_session(
        training_session_id
    )

    response = TrainingSessionSchema.model_validate(training_session)

    message = WebSocketMessage(
        type=MessageTypeEnum.TRAINING_FINISHED,
        payload=None,
    )

    await training_manager.broadcast(str(training_session_id), message.json())

    return response


@router.get(
    "/{training_session_id}/code/{alias}",
    status_code=status.HTTP_200_OK,
)
async def get_code(
    training_session_id: UUID,
    alias: str,
    redis_storage_manager: RedisStorageManager = Depends(),
) -> dict:
    code = redis_storage_manager.codesnap.get(training_session_id, alias)
    return {"code": code}


@router.get(
    "/{training_session_id}/control/current",
    status_code=status.HTTP_200_OK,
)
async def get_current_controller(
    training_session_id: UUID,
    redis_storage_manager: RedisStorageManager = Depends(),
) -> dict:
    user_id = redis_storage_manager.controller.get(training_session_id)
    return {"userId": user_id}


@router.get(
    "/{training_session_id}/online",
    status_code=status.HTTP_200_OK,
)
async def get_online_users(
    training_session_id: UUID,
    redis_storage_manager: RedisStorageManager = Depends(),
) -> dict:
    users = redis_storage_manager.training_users.get_users(training_session_id)
    return {"users": users}


@router.get(
    "/team/{team_id}/reconnect",
    status_code=status.HTTP_200_OK,
)
async def reconnect(
    team_id: int,
    training_session_repository: TrainingSessionRepository = Depends(),
) -> TrainingSessionSchema:
    training_session = await training_session_repository.get_active_training_by_team_id(
        team_id=str(team_id)
    )
    if not training_session:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return TrainingSessionSchema.model_validate(training_session)


@router.get(
    "/{training_session_id}/compiler/{alias}",
    status_code=status.HTTP_200_OK,
)
async def get_compiler(
    training_session_id: UUID,
    alias: str,
    redis_storage_manager: RedisStorageManager = Depends(),
) -> dict:
    compiler = redis_storage_manager.selected_compilers.get(training_session_id, alias)
    return {"compiler": compiler}
