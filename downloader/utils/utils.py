import os
from PySide6.QtGui import QIcon


def get_resource_path(resource: str):
    dir_name = os.getcwd()
    file_path = os.path.normpath(os.path.join(dir_name, resource))

    return file_path

def get_icon(name: str) -> QIcon:
    if not name:
        return None

    return QIcon(f":/icons/{name}.png")
