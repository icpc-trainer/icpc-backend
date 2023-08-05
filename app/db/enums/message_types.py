from enum import Enum


class MessageTypeEnum(str, Enum):
    USER_JOIN = "USER_JOIN"
    USER_LEAVE = "USER_LEAVE"
