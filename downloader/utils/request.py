import requests

from ..enums import Req
from ..settings import settings
from ..enums import SettingsKey


def get(url: str, **kwargs):
    headers = {
        "user-agent": Req.USER_AGENT.value,
        "referer": Req.REFERER.value,
        "cookie": settings.get(SettingsKey.COOKIE)
    }

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

def get_json(url: str, **kwargs):
    res = get(url, **kwargs)

    if res.status_code != 200:
        print(res.reason)
        
        ret = {
            "code": res.status_code,
            "message": res.reason
        }

        return ret
    
    return res.json()
