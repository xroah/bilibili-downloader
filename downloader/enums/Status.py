from enum import Enum


class Status(Enum):
    ERROR = "error"
    DONE = "done"
    UPDATE = "update"
    PAUSE = "pause"
    START = "start"
    MERGE = "merge"
    RESUME = "RESUME"
