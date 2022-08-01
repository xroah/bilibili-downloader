import os
from urllib.parse import urlparse
import re

from PySide6.QtGui import QIcon


def get_data_dir():
    return os.path.join(os.getcwd(), "data")


def get_resource_path(resource: str):
    dir_name = os.getcwd()
    file_path = os.path.join(dir_name, "resources", resource)

    return os.path.normpath(file_path)


def get_icon(name: str, ext="svg") -> QIcon | None:
    if not name:
        return None

    return QIcon(f":/icons/{name}.{ext}")


def get_style(name: str) -> str:
    file = get_resource_path(f"styles/{name}.qss")

    with open(file, "r") as f:
        ss = f.read()

    return ss


def get_default_download_path() -> str:
    home = os.path.expanduser("~")
    download_path = os.path.join(home, "Downloads")

    if not os.path.exists(download_path):
        os.makedirs(download_path)

    return download_path


def format_size(size: float) -> str:
    size_units = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    ret = size
    len_ = len(size_units)
    while ret >= 1024 and i < len_:
        ret /= 1024
        i += 1

    return f"{round(ret, 2)}{size_units[i]}"


def match_video_id(vid: str) -> bool:
    av_pattern = r"^av\d+$"
    bv_pattern = r"^bv[\da-zA-Z]{10}$"

    if (
            re.fullmatch(av_pattern, vid, re.IGNORECASE) or
            re.fullmatch(bv_pattern, vid, re.IGNORECASE)
    ):
        return True

    return False


def parse_url(url: str) -> str | None:
    if not url.strip():
        return

    matched = match_video_id(url)

    if matched:
        return url

    if "bilibili.com" not in url:
        return None

    # like: https://www.bilibili.com/video/BVxxxx
    parsed = urlparse(url)
    base = os.path.basename(parsed.path)
    matched = match_video_id(base)

    if matched:
        return base

    return None
