from fastapi import WebSocket
from starlette import status

from app.config import settings


class ConnectionManager:
    def __init__(self):
        self.connections = {}

    async def connect(self, websocket: WebSocket, key: str) -> bool:
        if key not in self.connections:
            self.connections[key] = set()

        await websocket.accept()

        if len(self.connections[key]) >= settings.MAX_CONNECTIONS_PER_GROUP:
            await websocket.close(
                code=status.WS_1008_POLICY_VIOLATION,
                reason="Превышен лимит подключений",
            )
            return False

        self.connections[key].add(websocket)
        return True

    def disconnect(self, websocket: WebSocket, key: str):
        if key in self.connections:
            self.connections[key].discard(websocket)

    async def send_message(self, websocket: WebSocket, message: str):
        await websocket.send_text(message)

    async def broadcast(self, key: str, message: str):
        if key in self.connections:
            for websocket in self.connections[key]:
                await self.send_message(websocket, message)
