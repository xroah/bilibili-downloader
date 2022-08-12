import os
import subprocess
import sys
from urllib.parse import urlparse
import re
from typing import (
    cast,
    TypeVar,
    Type,
    Tuple
)

from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QIcon, QGuiApplication


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


def get_style(*names: str) -> str:
    ss = ""
    for name in names:
        file = get_resource_path(f"styles/{name}.qss")

        try:
            with open(file, "r") as f:
                ss += f.read()
        except FileNotFoundError:
            pass

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


def center(
        widget: QWidget,
        parent: QWidget | bool
) -> Tuple[float, float]:
    size = widget.size()

    # center in screen
    if isinstance(parent, bool):
        screen = QGuiApplication.primaryScreen()
        avail_size = screen.availableSize()
        left = (avail_size.width() - size.width()) / 2
        top = (avail_size.height() - size.height()) / 2
    else:
        p_geometry = parent.frameGeometry()
        left = (p_geometry.width() - size.width()) / 2
        top = (p_geometry.height() - size.height()) / 2
        left += p_geometry.x()
        top += p_geometry.y()

    widget.move(left, top)

    return left, top


T = TypeVar("T", bound=QWidget)


def get_child(p: QWidget, t: Type[T], name: str) -> T:
    return cast(
        t,
        p.findChild(t, name)
    )


def open_path(path):
    if not os.path.exists(path):
        return

    platform = sys.platform
    if platform == "win32":
        os.startfile(path, "open")
    else:
        subprocess.call(("open", path))
