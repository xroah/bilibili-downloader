from .BaseEnum import BaseEnum

host = "https://www.bilibili.com"
api = "https://api.bilibili.com"


class Req(BaseEnum):
    REFERER = host
    USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36" \
                 "(KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
    PLAY_URL = f"{api}/x/player/wbi/playurl"
    # pages or sections
    VIEW_URL = f"{api}/x/web-interface/wbi/view"
    SEASON_URL = f"{api}/pgc/view/web/season"
    EP_PLAY_URL = f"{api}/pgc/player/web/playurl"
    VIDEO_PAGE = f"{host}/video"
