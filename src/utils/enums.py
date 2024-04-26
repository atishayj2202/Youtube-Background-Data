from enum import Enum


class CallStatus(Enum):
    NOT_FOUND = "NOT_FOUND"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"