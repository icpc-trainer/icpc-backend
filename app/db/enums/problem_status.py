from enum import Enum


class ProblemStatusEnum(str, Enum):
    NOT_SUBMITTED = "NOT_SUBMITTED"
    PASSED = "PASSED"
    FAILED = "FAILED"
