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
    team_id: int,
    contest_id: int,
    user_id: str,
):
    group = f"{team_id}_{contest_id}"

    is_connected = await manager.connect(websocket, group)

    if not is_connected:
        return

    message = WebSocketMessage(
        type=MessageTypeEnum.USER_JOIN,
        payload={"userId": user_id},
    )

    await manager.broadcast(group, message.json())

    try:
        while True:
            msg = await websocket.receive_text()

            await manager.broadcast(group, msg)
    except WebSocketDisconnect:
        manager.disconnect(websocket, group)
        message = WebSocketMessage(
            type=MessageTypeEnum.USER_LEAVE,
            payload={"userId": user_id},
        )
        await manager.broadcast(group, message.json())
