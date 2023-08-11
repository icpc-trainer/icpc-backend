from fastapi.testclient import TestClient
from app.__main__ import app


def test_websocket():
    client = TestClient(app)
    with client.websocket_connect("/ws/lobby?team_id=1&user_id=2") as websocket:
        data = websocket.receive_json()
        assert data == {"type": "USER_JOIN", "payload": {"userId": "2"}}
