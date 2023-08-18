from enum import Enum


class MessageTypeEnum(str, Enum):
    USER_JOIN = "USER_JOIN"
    USER_LEAVE = "USER_LEAVE"
    USER = "USER"
    SUBMISSION_VERDICT_RETRIEVED = "SUBMISSION_VERDICT_RETRIEVED"
    PROBLEM_STATUS_UPDATED = "PROBLEM_STATUS_UPDATED"
    CODE_EDITOR_UPDATE = "CODE_EDITOR_UPDATE"
    PROBLEM_COMMENT_RECEIVED = "PROBLEM_COMMENT_RECEIVED"
    CONTROL_TAKEN = "CONTROL_TAKEN"
    TRAINING_STARTED = "TRAINING_STARTED"
    TRAINING_FINISHED = "TRAINING_FINISHED"
    PROBLEM_ASSIGNED = "PROBLEM_ASSIGNED"
    CONTEST_SELECTED = "CONTEST_SELECTED"
