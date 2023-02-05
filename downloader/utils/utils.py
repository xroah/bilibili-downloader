import os
import subprocess
import sys
from urllib.parse import urlparse
import re


def get_data_dir():
    return os.path.join(os.getcwd(), "data")


def get_resource_path(resource: str):
    dir_name = os.getcwd()
    file_path = os.path.join(dir_name, "resources", resource)

    return os.path.normpath(file_path)


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
