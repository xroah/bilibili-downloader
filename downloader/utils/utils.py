import os
from urllib.parse import urlparse
import re
import shutil

from PySide6.QtGui import QIcon


def get_data_dir():
    return os.path.join(os.getcwd(), "data")


def get_resource_path(resource: str):
    dir_name = os.getcwd()
    file_path = os.path.join(dir_name, "resources", resource)

    return os.path.normpath(file_path)


def get_icon(name: str, ext="svg", string=False) -> QIcon | None:
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


def get_size(path: str) -> float:
    size = os.path.getsize(path)
    files = os.scandir(path)

    if os.path.ismount(path):
        usage = shutil.disk_usage(path)

        return usage.used

    for f in files:
        f_path = os.path.join(path, f.name)
        size += os.path.getsize(f_path)
        if f.is_dir():
            size += get_size(f)

    return size


def format_size(size: float) -> str:
    size_units = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    ret = size
    len_ = len(size_units)
    while ret >= 1024 and i < len_:
        ret /= 1024
        i += 1

    return f"{round(ret, 2)}{size_units[i]}"


def parse_url(url: str) -> str | None:
    if not url.strip():
        return

    pattern = r"^(BV|AV)[\da-zA-z]+$"  # bv no pattern

    def fullmatch(s):
        return re.fullmatch(pattern, s, re.IGNORECASE)

    matched = fullmatch(url)

    if matched:
        return matched.string

    # like: https://www.bilibili.com/video/BVxxxx
    parsed = urlparse(url)

    if not parsed.hostname or "bilibili" not in parsed.hostname:
        return None

    base = os.path.basename(parsed.path)
    matched = fullmatch(base)

    if matched:
        return matched.string

    return None
