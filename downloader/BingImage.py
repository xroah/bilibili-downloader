from bs4 import BeautifulSoup
import httpx
from PIL import Image
from PIL.ImageFilter import GaussianBlur

import os
import os.path
from typing import Callable
import time

from .App import App

bing_host = "https://cn.bing.com"


def get_img_url() -> str:
    res = httpx.get(bing_host)
    soup = BeautifulSoup(res.text, "html.parser")
    ret = soup.select("#preloadBg")

    if len(ret) >= 1:
        return ret[0]["href"]

    return ""


def blur_img(img_dir: str, img_name: str) -> str:
    full_path = os.path.join(img_dir, img_name)

    with Image.open(full_path) as img:
        new_img = img.filter(GaussianBlur(25))
        new_img.save(os.path.join(img_dir, img_name), "png")


def download_img(callback: Callable[[str, App], None]) -> None:
    cwd = os.getcwd()
    tmp = os.path.join(cwd, "tmp")
    name = time.strftime("%Y%m%d") + ".png"
    full_name = os.path.join(tmp, name)
    downloaded = False

    if not os.path.exists(tmp):
        os.mkdir(tmp)
    else:
        files = os.scandir(tmp)

        for f in files:
            if f.is_file():
                if f.name == name:
                    downloaded = True
                else:
                    os.unlink(os.path.join(tmp, f.name))

    if downloaded:
        return callback(full_name)

    img_url = get_img_url()

    if img_url:
        res = httpx.get(img_url)
        with open(full_name, "wb") as f:
            f.write(res.content)
        blur_img(tmp, name)
        callback(full_name)
