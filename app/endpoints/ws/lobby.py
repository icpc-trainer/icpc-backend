import json

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.db.enums import MessageTypeEnum
from app.services import lobby_manager as manager


router = APIRouter(
    prefix="/ws",
    tags=["Lobby"],
)


@router.websocket("/lobby")
async def lobby(
    websocket: WebSocket,
    team_id: int,
    user_id: str,
):
    group = team_id

    is_connected = await manager.connect(websocket, group)

    if not is_connected:
        return

    message = {
        "type": MessageTypeEnum.USER_JOIN,
        "data": {"userId": user_id},
    }

    await manager.broadcast(group, json.dumps(message))

    try:
        while True:
            msg = await websocket.receive_text()

            await manager.broadcast(group, msg)
    except WebSocketDisconnect:
        manager.disconnect(websocket, group)
        message = {
            "type": MessageTypeEnum.USER_LEAVE,
            "data": {"userId": user_id},
        }
        await manager.broadcast(group, json.dumps(message))
