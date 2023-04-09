import os
import subprocess
import sys


def get_data_dir():
    home = os.path.expanduser("~")
    data_dir = os.path.join(home, ".bilibili-downloader")

    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    return data_dir


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


def open_path(path):
    if not os.path.exists(path):
        return

    platform = sys.platform
    if platform == "win32":
        os.startfile(path, "open")
    else:
        subprocess.call(("open", path))
