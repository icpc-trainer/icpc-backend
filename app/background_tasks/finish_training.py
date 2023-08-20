import asyncio
from uuid import UUID
from datetime import timedelta

from app.services import TrainingSessionRepository, training_manager

from app.utils import WebSocketMessage
from app.db.enums import MessageTypeEnum


async def training_session_finisher(
    wait_time: timedelta,
    training_session_id: UUID,
    training_session_repository: TrainingSessionRepository,
) -> None:
    await asyncio.sleep(wait_time.total_seconds())
    await training_session_repository.complete_training_session(
        training_session_id=training_session_id
    )
    message = WebSocketMessage(
        type=MessageTypeEnum.CONTEST_FINISHED,
        payload=None,
    )
    await training_manager.broadcast(str(training_session_id), message.json())
