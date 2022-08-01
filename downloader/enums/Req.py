from enum import Enum


class Req(Enum):
    REFERER = "https://www.bilibili.com"
    USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
    API_ADDR = "https://api.bilibili.com/x/player/"
    LIST_PATH = "pagelist"
    URL_PATH = "playurl"
    VIDEO_PAGE = "https://www.bilibili.com/video/"
    CHECK_LOGIN = "https://api.bilibili.com/x/web-interface/nav"
    LOGIN_PAGE = "https://passport.bilibili.com/ajax/miniLogin/minilogin"

    def __str__(self) -> str:
        return self.value