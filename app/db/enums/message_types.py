from enum import Enum


class MessageTypeEnum(str, Enum):
    USER_JOIN = "USER_JOIN"
    USER_LEAVE = "USER_LEAVE"
    SUBMISSION_VERDICT_RETRIEVED = "SUBMISSION_VERDICT_RETRIEVED"
    SUBMISSION_VERDICT_PENDING = "SUBMISSION_VERDICT_PENDING"
    CODE_EDITOR_UPDATE = "CODE_EDITOR_UPDATE"
    PROBLEM_COMMENT_RECEIVED = "PROBLEM_COMMENT_RECEIVED"
