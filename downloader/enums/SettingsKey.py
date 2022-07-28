from enum import Enum


class SettingsKey(Enum):
    DOWNLOAD_PATH = "download_path"
    IS_SHOW_MESSAGE = "is_show_message"
    IS_PLAY_RINGTONE = "is_play_ringtone"
    IS_MONITOR_CLIPBOARD = "is_monitor_clipboard"
    IS_AUTO_DOWNLOAD = "is_auto_download"

    def __str__(self):
        return self.value

