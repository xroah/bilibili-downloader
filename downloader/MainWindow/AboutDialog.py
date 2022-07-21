from ..CommonWidgets import Dialog
from ..utils import utils

import __main__

import sys
from PySide6 import __version__
from PySide6.QtCore import QSize
from PySide6.QtWidgets import (
    QLabel,
    QWidget,
    QVBoxLayout,
    QMainWindow, 
    QDialog
)

def get_python_ver():
    ver = sys.version_info
    return "{0}.{1}.{2}".format(ver.major, ver.minor, ver.micro)

def create_about_dialog(window: QMainWindow) -> None:
    dialog = Dialog(
        window,
        QSize(260, 200),
        "关于"
    )
    filename = utils.get_resource_path("about.html")

    with open(filename, "r", encoding="utf-8") as f:
        text = f.read().format(
            ver=__main__.__version__,
            pyside_ver=__version__,
            python_ver=get_python_ver()
        )

    w = QWidget(dialog.body)
    about = QLabel()
    layout = QVBoxLayout(w)
    about.setText(text)
    about.setOpenExternalLinks(True)
    layout.addWidget(about)
    w.setLayout(layout)
    dialog.set_content(w)

    dialog.open_()

    return dialog