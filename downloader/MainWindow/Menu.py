import sys
from typing import Callable

from PySide6.QtCore import QSize, __version__
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QMenu,
    QWidget,
    QLabel,
    QVBoxLayout,
    QMainWindow
)

import __main__
from ..Dialog import Dialog
from ..utils import utils


class Menu(QMenu):
    def __init__(self, window: QMainWindow,  parent: QWidget = None):
        super().__init__(parent)
        self.window = window
        self.init()

    def init(self):
        self.add_action("关于", self.about_action)
        self.add_action("退出", lambda: sys.exit(0))
        with open(utils.get_resource_path("styles/menu.qss")) as ss:
            self.setStyleSheet(ss.read())

    def add_action(
            self,
            text: str,
            cb: Callable[[bool], None]
    ) -> QAction:
        action = self.addAction(text)

        if cb is not None:
            action.triggered.connect(cb)

        return action

    def about_action(self):
        dialog = Dialog(
            self.window,
            QSize(260, 200),
            "关于"
        )
        filename = utils.get_resource_path("resources/about.html")

        with open(filename, "r", encoding="utf-8") as f:
            text = f.read().format(
                v=__main__.__version__,
                pv=__version__
            )

        w = QWidget(dialog.body)
        about = QLabel()
        layout = QVBoxLayout(w)
        about.setText(text)
        about.setOpenExternalLinks(True)
        layout.addWidget(about)
        w.setLayout(layout)

        dialog.set_content(w)
        dialog.open()
