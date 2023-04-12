import os
import json
from typing import cast, Any

from ..utils import utils
from ..enums import SettingsKey

_settings_dir = utils.get_data_dir()
_settings_file = os.path.join(_settings_dir, "settings.json")
_default_settings = {
    str(SettingsKey.DOWNLOAD_PATH): utils.get_default_download_path(),
    str(SettingsKey.COOKIE): ""
}


class Settings:
    def __init__(self) -> None:
        self._dict = self.get_all()

    @staticmethod
    def get_all() -> dict:
        settings = _default_settings.copy()

        if not os.path.exists(_settings_file):
            return settings

        try:
            with open(_settings_file, "r") as f:
                d = cast(dict, json.load(f))
        except Exception as e:
            print("Load settings error:", e)
            return settings

        for k, v in d.items():
            if k in settings and k in _default_settings and v:
                settings[k] = v

        return settings

    def save(self) -> None:
        try:
            with open(_settings_file, "w") as f:
                json.dump(self._dict, f, indent=4)
        except Exception as e:
            print("Save settings error:", e)

    def get(self, name: str | SettingsKey) -> Any:
        key = str(name)

        if key not in self._dict:
            return None

        return self._dict[key]

    def set(self, name: str | SettingsKey, value: Any) -> bool:
        key = str(name)

        if key not in self._dict:
            print("Invalid settings key.")
            return False

        if not value:
            print("The value can not be empty")
            return False

        if self._dict[key] == value:
            return False

        self._dict[key] = value

        self.save()

        return True
