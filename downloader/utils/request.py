import httpx

from ..cookie import Cookie
from ..enums import Req


def get(url: str, **kwargs):
    cookie = Cookie()
    headers = {
        "cookie": cookie.cookie,
        "user-agent": Req.USER_AGENT.value,
        "referer": Req.REFERER.value
    }
    if "headers" in kwargs:
        for k, v in kwargs.items():
            headers[k] = v
        del kwargs["headers"]

    try:
        res = httpx.get(url, headers=headers, **kwargs)
    except Exception as E:
        print(f"Request {url} error: ", E.args)
        raise E
    else:
        return res
