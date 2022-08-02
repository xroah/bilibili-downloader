from typing import Callable

from PySide6.QtGui import QAction, QShowEvent, QCursor
from PySide6.QtWidgets import (
    QWidget,
    QMainWindow,
    QToolButton
)

from ..common_widgets import Menu
from ..utils import utils
from .AboutDialog import create_about_dialog
from ..actions import get_settings_action, get_quit_action


class MainMenu(Menu):
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
        get_settings_action(self, "settings")
        self.add_action("关于", "about", self.about_action)
        get_quit_action(self, "exit")

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

    def about_action(self):
        create_about_dialog(self._window)

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

