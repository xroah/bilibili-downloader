import os
from PySide6.QtGui import QIcon


def get_resource_path(resource: str):
    dir_name = os.getcwd()
    file_path = os.path.join(dir_name, "resources", resource)

    return os.path.normpath(file_path)


def get_icon(name: str, ext: str = "svg") -> QIcon | None:
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
