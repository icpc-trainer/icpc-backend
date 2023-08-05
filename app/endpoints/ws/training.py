import json
from typing import Annotated

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends

from app.db.enums import MessageType
from app.services import ConnectionManager


router = APIRouter(
    prefix="/ws",
    tags=["Training"],
)


@router.websocket("/training")
async def training(
    websocket: WebSocket,
    manager: Annotated[ConnectionManager, Depends(ConnectionManager)],
    team_id: int,
    user_id: int,
):
    await manager.connect(websocket, team_id)

    message = {
        "type": MessageType.USER_JOIN,
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
            "type": MessageType.USER_LEAVE,
            "data": {"userId": user_id},
        }
        await manager.broadcast(json.dumps(message), team_id)
