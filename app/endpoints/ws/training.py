from uuid import UUID
import asyncio

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.db.enums import MessageTypeEnum
from app.services import training_manager as manager
from app.utils import WebSocketMessage
from app.services import redis_storage_manager


router = APIRouter(
    prefix="/ws",
    tags=["Training"],
)


async def handle_message(training_session_id, message_data):
    """
    Функция обрабатывает входящие сообщения
    """
    is_validated, message =  WebSocketMessage.validate(message_data)

    if not is_validated:
        return

    if message.type == MessageTypeEnum.CODE_EDITOR_UPDATE:
        redis_storage_manager.codesnap.set(
            training_session_id,
            message.payload['problemAlias'],
            message.payload['code'],
        )
    elif message.type == MessageTypeEnum.CONTROL_TAKEN:
        redis_storage_manager.controllers.set(
            training_session_id,
            message.payload['userId'],
        )


@router.websocket("/training")
async def training(
    websocket: WebSocket,
    training_session_id: UUID,
    user_id: str,
):
    is_connected = await manager.connect(websocket, str(training_session_id))

    if not is_connected:
        return

    message = WebSocketMessage(
        type=MessageTypeEnum.USER_JOIN,
        payload={"userId": user_id},
    )

    await manager.broadcast(str(training_session_id), message.json())
    try:
        while True:
            msg = await websocket.receive_text()

            asyncio.create_task(handle_message(str(training_session_id), msg))

            await manager.broadcast(str(training_session_id), msg)
    except WebSocketDisconnect:
        manager.disconnect(websocket, str(training_session_id))
        message = WebSocketMessage(
            type=MessageTypeEnum.USER_LEAVE,
            payload={"userId": user_id},
        )
        await manager.broadcast(str(training_session_id), message.json())
