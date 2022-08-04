import os

from downloader.utils import utils, event_bus
from downloader.utils.Singleton import Singleton
from downloader.enums import EventName


class Cookie(Singleton):
    def __init__(self):
        self.cookie = self._get_all()

    @staticmethod
    def get_cookie_file():
        filename = "cookie.txt"
        data_dir = utils.get_data_dir()
        full_path = os.path.join(data_dir, filename)

        return full_path

    def _get_all(self) -> str:
        cookie_file = self.get_cookie_file()

        if not os.path.exists(cookie_file):
            return ""

        with open(cookie_file, "r") as f:
            return f.read()

    def set(self, v: str):
        if self.cookie == v:
            return

        cookie_file = self.get_cookie_file()
        self.cookie = v
        with open(cookie_file, "w") as f:
            f.write(v)
        event_bus.emit(EventName.COOKIE_CHANGE)

    def delete(self):
        cookie_file = self.get_cookie_file()
        if os.path.exists(cookie_file):
            self.cookie = ""
            os.unlink(cookie_file)