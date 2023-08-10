import json
from dataclasses import dataclass

from app.db.enums import MessageTypeEnum


@dataclass
class WebSocketMessage:
    type: MessageTypeEnum
    payload: dict

    def json(self):
        return json.dumps(self.__dict__)

    @staticmethod
    def validate(message_data):
        try:
            message_dict = json.loads(message_data)
            websocket_message = WebSocketMessage(**message_dict)
            return True, websocket_message
        except (json.JSONDecodeError, TypeError) as e:
            return False, None
