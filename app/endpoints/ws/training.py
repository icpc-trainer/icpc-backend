import json

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends

from app.db.enums import MessageType
from app.services import training_manager as manager


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
    store_key = f"{team_id}_{contest_id}"

    await manager.connect(websocket, store_key)

    message = {
        "type": MessageType.USER_JOIN,
        "data": {"userId": user_id},
    }

    await manager.broadcast(json.dumps(message), store_key)

    try:
        while True:
            msg = await websocket.receive_json()

            await manager.broadcast(json.dumps(msg), store_key)
    except WebSocketDisconnect:
        manager.disconnect(websocket, store_key)
        message = {
            "type": MessageType.USER_LEAVE,
            "data": {"userId": user_id},
        }
        await manager.broadcast(json.dumps(message), store_key)
