import json

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends

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
    await manager.connect(websocket, team_id)

    message = {
        "type": MessageTypeEnum.USER_JOIN,
        "data": {"userId": user_id},
    }

    await manager.broadcast(json.dumps(message), team_id)

    try:
        while True:
            msg = await websocket.receive_json()

            await manager.broadcast(json.dumps(msg), team_id)
    except WebSocketDisconnect:
        manager.disconnect(websocket, team_id)
        message = {
            "type": MessageTypeEnum.USER_LEAVE,
            "data": {"userId": user_id},
        }
        await manager.broadcast(json.dumps(message), team_id)
