from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.db.enums import MessageTypeEnum
from app.services import lobby_manager as manager
from app.utils import WebSocketMessage


router = APIRouter(
    prefix="/ws",
    tags=["Lobby"],
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

            await manager.broadcast(team_id, msg)
    except WebSocketDisconnect:
        manager.disconnect(websocket, team_id)
        message = WebSocketMessage(
            type=MessageTypeEnum.USER_LEAVE,
            payload={"userId": user_id},
        )
        await manager.broadcast(team_id, message.json())
