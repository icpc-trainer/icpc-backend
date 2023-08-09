from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.db.enums import MessageTypeEnum
from app.services import training_manager as manager
from app.utils import WebSocketMessage


router = APIRouter(
    prefix="/ws",
    tags=["Training"],
)


@router.websocket("/training")
async def training(
    websocket: WebSocket,
    training_session_id: int,
    user_id: str,
):
    is_connected = await manager.connect(websocket, training_session_id)

    if not is_connected:
        return

    message = WebSocketMessage(
        type=MessageTypeEnum.USER_JOIN,
        payload={"userId": user_id},
    )

    await manager.broadcast(training_session_id, message.json())

    try:
        while True:
            msg = await websocket.receive_text()

            await manager.broadcast(training_session_id, msg)
    except WebSocketDisconnect:
        manager.disconnect(websocket, training_session_id)
        message = WebSocketMessage(
            type=MessageTypeEnum.USER_LEAVE,
            payload={"userId": user_id},
        )
        await manager.broadcast(training_session_id, message.json())
