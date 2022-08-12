from enum import Enum


class EventName(Enum):
    # create a new download
    NEW_DOWNLOAD = "new_download"
    COOKIE_CHANGE = "cookie_change"
    CHECK_ALL = "check_all"
    DATA_INITIALIZED = "data_initialized"
    DOWNLOAD_FINISHED = "download_finished"
