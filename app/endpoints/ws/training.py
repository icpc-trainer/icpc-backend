import json

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends

from app.db.enums import MessageTypeEnum
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
    group = f"{team_id}_{contest_id}"

    await manager.connect(websocket, group)

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
