from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        self.connections = {}

    async def connect(self, websocket: WebSocket, key: str):
        await websocket.accept()
        if key not in self.connections:
            self.connections[key] = set()
        self.connections[key].add(websocket)

    def disconnect(self, websocket: WebSocket, key: str):
        if key in self.connections:
            self.connections[key].discard(websocket)

    async def send_message(self, websocket: WebSocket, message: str):
        await websocket.send_text(message)

    async def broadcast(self, key: str, message: str):
        if key in self.connections:
            for websocket in self.connections[key]:
                await self.send_message(websocket, message)
