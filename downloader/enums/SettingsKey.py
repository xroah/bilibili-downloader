from enum import Enum


class SettingsKey(Enum):
    DOWNLOAD_PATH = "path"

    def __str__(self):
        return self.value

