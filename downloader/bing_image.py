import os
import os.path
import time

from bs4 import BeautifulSoup
import requests

from .enums import Req

bing_host = "https://cn.bing.com"
cwd = os.getcwd()
bg_dir = os.path.join(cwd, "bg")


def request(url, i=0):
    try:
        res = requests.get(
            url,
            timeout=15,
            headers={
                "referer": "https://cn.bing.com",
                "user-agent": Req.USER_AGENT.value
            }
        )
    except:
        i += 1

        if i < 10:
            return request(url, i)
    else:
        return res


def get_img_url() -> str:
    res = request(bing_host)
    soup = BeautifulSoup(res.text, "html.parser")
    ret = soup.select("#preloadBg")

    if len(ret) >= 1:
        return ret[0]["href"]

    return ""


def check(name: str) -> bool:
    if not os.path.exists(bg_dir):
        os.mkdir(bg_dir)
        return False

    files = os.scandir(bg_dir)
    downloaded = False

    for f in files:
        if f.is_file():
            if f.name == name:
                downloaded = True
            else:
                os.unlink(os.path.join(bg_dir, f.name))

    return downloaded


def get_img_path():
    name = time.strftime("%Y-%m-%d") + ".png"
    path = os.path.join(bg_dir, name)

    return name, path


def download_img() -> str:
    name, full_name = get_img_path()

    if check(name):
        return full_name

    img_url = get_img_url()

    if img_url:
        res = request(img_url)
        with open(full_name, "wb") as f:
            f.write(res.content)

        return full_name

    return ""
