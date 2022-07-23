from bs4 import BeautifulSoup
import httpx
from PIL import Image
from PIL.ImageFilter import GaussianBlur

import os
import os.path
from typing import Callable
import time
import io

bing_host = "https://cn.bing.com"
cwd = os.getcwd()
bg_dir = os.path.join(cwd, "bg")


def get_img_url() -> str:
    res = httpx.get(bing_host)
    soup = BeautifulSoup(res.text, "html.parser")
    ret = soup.select("#preloadBg")

    if len(ret) >= 1:
        return ret[0]["href"]

    return ""


def blur_img(img: io.BytesIO, img_name: str) -> str:
    img_path = os.path.join(bg_dir, img_name)
    with Image.open(img,) as _img:
        new_img = _img.filter(GaussianBlur(25))
        new_img.save(img_path)


def download_img(callback: Callable[[str], None]) -> None:
    name = time.strftime("%Y%m%d") + ".png"
    full_name = os.path.join(bg_dir, name)
    downloaded = False

    if not os.path.exists(bg_dir):
        os.mkdir(bg_dir)
    else:
        files = os.scandir(bg_dir)

        for f in files:
            if f.is_file():
                if f.name == name:
                    downloaded = True
                else:
                    os.unlink(os.path.join(bg_dir, f.name))

    if downloaded:
        return callback(full_name)

    img_url = get_img_url()

    if img_url:
        res = httpx.get(img_url)
        blur_img(io.BytesIO(res.content), name)
        callback(full_name)
