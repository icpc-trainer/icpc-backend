import asyncio

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.db.enums import MessageTypeEnum
from app.services import lobby_manager as manager, redis_storage_manager
from app.utils import WebSocketMessage


router = APIRouter(
    prefix="/ws",
    tags=["Lobby"],
)

async def handle_message(team_id, message_data):
    """
    Функция обрабатывает входящие сообщения
    """
    is_validated, message =  WebSocketMessage.validate(message_data)

    if not is_validated:
        return

    if message.type == MessageTypeEnum.USER:
        redis_storage_manager.lobby_users.add_user(
            team_id,
            message.payload["user"],
        )


@router.websocket("/lobby")
async def lobby(
    websocket: WebSocket,
    team_id: str,
    user_id: str,
) -> None:
    is_connected = await manager.connect(websocket, team_id)

    if not is_connected:
        return

    message = WebSocketMessage(
        type=MessageTypeEnum.USER_JOIN,
        payload={"userId": user_id},
    )

    await manager.broadcast(team_id, message.json())

    try:
        while True:
            msg = await websocket.receive_text()

            asyncio.create_task(handle_message(str(team_id), msg))

            await manager.broadcast(team_id, msg)
    except WebSocketDisconnect:
        manager.disconnect(websocket, team_id)
        message = WebSocketMessage(
            type=MessageTypeEnum.USER_LEAVE,
            payload={"userId": user_id},
        )
        redis_storage_manager.lobby_users.remove_user(team_id, user_id)
        await manager.broadcast(team_id, message.json())
