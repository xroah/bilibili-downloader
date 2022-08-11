import requests

from ..cookie import cookie
from ..enums import Req

headers = {
    "cookie": cookie.cookie,
    "user-agent": Req.USER_AGENT.value,
    "referer": Req.REFERER.value
}


def get(url: str, **kwargs):
    global headers

    if "headers" in kwargs:
        for k, v in kwargs["headers"].items():
            headers[k] = v
        del kwargs["headers"]

    try:
        res = requests.get(url, headers=headers, **kwargs)
    except Exception as E:
        print(f"Request {url} error: ", E.args)
        raise E
    else:
        return res


def head(url):
    return requests.head(url, headers=headers)
