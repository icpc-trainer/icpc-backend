from typing import Dict, List
from fastapi import WebSocket


class ConnectionManager:
    def __init__(self) -> None:
        self.active_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, webscoket: WebSocket, key: str):
        await webscoket.accept()
        if key in self.active_connections:
            self.active_connections[key].append(webscoket)
        else:
            self.active_connections[key] = [webscoket]

    def disconnect(self, websocket: WebSocket, key: str):
        if key in self.active_connections:
            self.active_connections[key].remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str, key: str):
        if key in self.active_connections:
            for connection in self.active_connections[key]:
                await connection.send_text(message)
