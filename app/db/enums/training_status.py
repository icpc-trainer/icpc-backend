from enum import Enum


class TrainingStatusEnum(str, Enum):
    IN_PROCESS = "IN_PROCESS"
    FINISHED = "FINISHED"