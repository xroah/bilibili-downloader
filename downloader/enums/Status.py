from .BaseEnum import BaseEnum


class Status(BaseEnum):
    ERROR = "error"
    DONE = "done"
    UPDATE = "update"
    PAUSE = "pause"
    START = "start"
    MERGE = "merge"
