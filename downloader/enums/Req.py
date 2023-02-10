from enum import Enum

host = "https://www.bilibili.com"
api = f"{host}/x/player"


class Req(Enum):
    REFERER = host
    USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"\
                 " (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
    API_ADDR = api
    PLAY_URL = f"{api}/playurl"
    VIDEO_PAGE = f"{host}/video"
    CHECK_LOGIN = "https://api.bilibili.com/x/web-interface/nav"

    def __str__(self) -> str:
        return self.value
