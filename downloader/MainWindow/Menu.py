import sys
from typing import Callable

from PySide6.QtCore import QSize, __version__
from PySide6.QtGui import QAction, QShowEvent, QCursor
from PySide6.QtWidgets import (
    QMenu,
    QWidget,
    QLabel,
    QVBoxLayout,
    QMainWindow,
    QToolButton
)

import __main__
from ..Dialog import Dialog
from ..utils import utils


class Menu(QMenu):
    def __init__(
        self,
        window: QMainWindow,
        parent: QWidget = None,
        related_btn: QToolButton = None
    ):
        super().__init__(parent)
        self.related_btn = related_btn
        self._window = window
        self.init()

    def init(self):
        self.add_action("设置", "settings", self.settings_action)
        self.add_action("关于", "about", self.about_action)
        self.add_action("退出", "exit", lambda: sys.exit(0))
        with open(utils.get_resource_path("styles/menu.qss")) as ss:
            self.setStyleSheet(ss.read())

    def add_action(
            self,
            text: str,
            icon: str,
            cb: Callable[[bool], None] = None
    ) -> QAction:
        action = self.addAction(text)
        action.setIcon(utils.get_icon(icon))

        if cb is not None:
            action.triggered.connect(cb)

        return action

    def settings_action(self):
        print("settings")

    def about_action(self):
        dialog = Dialog(
            self._window,
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

    def showEvent(self, event: QShowEvent) -> None:
        super().showEvent(event)
        point = QCursor.pos()
        size = self.size()
        x = point.x() - size.width()
        y = point.y()
        
        if self.related_btn:
            win_rect = self._window.geometry()
            rect = self.related_btn.geometry()
            offset_y = point.y() - win_rect.y() - rect.y()
            offset_x = point.x() - win_rect.x() - rect.x()
            x += rect.width() - offset_x
            y += rect.height() - offset_y

        self.move(x, y)

