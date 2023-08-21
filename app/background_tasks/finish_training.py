import asyncio
from datetime import timedelta
from uuid import UUID

from app.db.enums import MessageTypeEnum
from app.services import TrainingSessionRepository, training_manager
from app.utils import WebSocketMessage


async def training_session_finisher(
    wait_time: timedelta,
    training_session_id: UUID,
    training_session_repository: TrainingSessionRepository,
) -> None:
    await asyncio.sleep(wait_time.total_seconds())
    training_session = await training_session_repository.complete_training_session(
        training_session_id=training_session_id
    )
    message = WebSocketMessage(
        type=MessageTypeEnum.CONTEST_FINISHED,
        payload={
            "id": str(training_session.id),
            "teamId": str(training_session.team.external_id),
            "contestId": str(training_session.contest.external_id),
            "status": training_session.status,
        },
    )
    await training_manager.broadcast(str(training_session_id), message.json())
