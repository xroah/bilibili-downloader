from enum import Enum


class SettingsKey(Enum):
    DOWNLOAD_PATH = "download_path"

    def __str__(self):
        return self.value

