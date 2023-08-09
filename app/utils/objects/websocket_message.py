import json
from dataclasses import dataclass

from app.db.enums import MessageTypeEnum


@dataclass
class WebSocketMessage:
    type: MessageTypeEnum
    payload: dict

    def json(self):
        return json.dumps(self.__dict__)
