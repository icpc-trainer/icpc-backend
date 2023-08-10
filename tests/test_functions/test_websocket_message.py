import pytest
from app.utils import WebSocketMessage


@pytest.mark.parametrize(
    "message_data, expected_validation_result",
    [
        ('{"type": "USER_JOIN", "payload": {}}', True),
        ('{"type": "USER_JOIN", "data": {}}', False),
        ('{"key": "USER_JOIN", "payload": {}}', False),
        ('{"type": "USER_JOIN"', False),
        ('{"payload": {}}', False),
    ],
)
def test_websocket_message(message_data, expected_validation_result):
    is_validated, _ = WebSocketMessage.validate(message_data)
    assert is_validated == expected_validation_result
