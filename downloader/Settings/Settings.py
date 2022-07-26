import os
import json
from typing import cast

from ..utils.decorators import singleton

from ..utils import utils

_settings_dir = os.path.join(os.getcwd(), "data")
_settings_file = os.path.join(_settings_dir, "settings.json")
_default_settings = {
    "download_path": utils.get_default_download_path(),
    "is_show_message": True,
    "is_play_ringtone": True,
    "is_monitor_clipboard": True
}


@singleton
class Settings:
    def __init__(self) -> None:
        self._dict = self.get_settings()

    def get_settings(self) -> dict:
        settings = _default_settings.copy()

        if not os.path.exists(_settings_dir):
            os.mkdir(_settings_dir)

        if not os.path.exists(_settings_file):
            self.save_settings(settings)
            return settings

        try:
            with open(_settings_file, "r") as f:
                d = cast(dict, json.load(f))
        except Exception as e:
            print("Load error:", e)
            return settings

        for k, v in d.items():
            if k in settings:
                settings[k] = v

        return settings

    def save_settings(self) -> None:
        try:
            with open(_settings_file, "w") as f:
                json.dump(self._dict, f, indent=4)
        except Exception as e:
            print("Save error:", e)

    def get(self, name: str) -> any:
        if not name in self._dict:
            return None

        return self._dict[name]

    def set(self, name: str, value: any):
        if not name in self._dict and self._dict[name] != value:
            return
            
        self._dict[name] = value
        self.save_settings()
