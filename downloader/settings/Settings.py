import os
import json
from typing import cast

from ..utils.Singleton import Singleton
from ..utils import utils
from ..enums import SettingsKey

_settings_dir = utils.get_data_dir()
_settings_file = os.path.join(_settings_dir, "settings.json")
_default_settings = {
    SettingsKey.DOWNLOAD_PATH.value: utils.get_default_download_path(),
    SettingsKey.IS_SHOW_MESSAGE.value: True,
    SettingsKey.IS_PLAY_RINGTONE.value: True,
    SettingsKey.IS_AUTO_DOWNLOAD.value: True
}


class Settings(Singleton):
    def __init__(self) -> None:
        self._dict = self.get_all()

    def get_all(self) -> dict:
        settings = _default_settings.copy()

        if not os.path.exists(_settings_file):
            self.save()
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

    def save(self) -> None:
        try:
            with open(_settings_file, "w") as f:
                json.dump(self._dict, f, indent=4)
        except Exception as e:
            print("Save error:", e)

    def get(self, name: str | SettingsKey) -> any:
        key = str(name)

        if key not in self._dict:
            return None

        return self._dict[key]

    def set(self, name: str | SettingsKey, value: any):
        key = str(name)

        if key not in self._dict and self._dict[key] != value:
            return

        self._dict[key] = value
