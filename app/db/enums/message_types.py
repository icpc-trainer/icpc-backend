from enum import Enum


class MessageType(str, Enum):
    USER_JOIN = "userJoin"
    USER_LEAVE = "userLeave"
