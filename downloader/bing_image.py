from bs4 import BeautifulSoup
import requests

import os
import os.path
import time

bing_host = "https://cn.bing.com"
cwd = os.getcwd()
bg_dir = os.path.join(cwd, "bg")


def get_img_url() -> str:
    res = requests.get(bing_host)
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


def download_img() -> str:
    name = time.strftime("%Y%m%d") + ".png"
    full_name = os.path.join(bg_dir, name)

    if check(name):
        return full_name

    img_url = get_img_url()

    if img_url:
        res = requests.get(img_url)
        with open(full_name, "wb") as f:
            f.write(res.content)

        return full_name

    return ""
