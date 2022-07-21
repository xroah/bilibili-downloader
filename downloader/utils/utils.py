import os
from PySide6.QtGui import QIcon
from PySide6.QtCore import QFile


def get_resource_path(resource: str):
    dir_name = os.getcwd()
    file_path = os.path.join(dir_name, "resources", resource)

    return os.path.normpath(file_path)


def get_icon(name: str) -> QIcon:
    if not name:
        return None

    return QIcon(f":/icons/{name}.png")


def get_style(name: str) -> str:
    file = QFile(f":/styles/{name}.qss")

    if not file.open(QFile.ReadOnly | QFile.Text):
        return ""

    ss = file.readAll()
    file.close()

    return ss.toStdString()
