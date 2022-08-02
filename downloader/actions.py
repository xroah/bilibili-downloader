from typing import Callable
import sys

from PySide6.QtWidgets import QMenu
from PySide6.QtGui import QAction
from PySide6.QtCore import Qt, QTimer

from .settings import SettingsDialog
from .utils import utils


class Action:
    _settings_dialog = None

    @staticmethod
    def quit_app():
        sys.exit(0)

    @classmethod
    def _dialog_close(cls):
        cls._settings_dialog = None

    @classmethod
    def show_settings(cls):
        if cls._settings_dialog is None:
            cls._settings_dialog = SettingsDialog()

        cls._settings_dialog.showNormal()
        cls._settings_dialog.setWindowState(Qt.WindowActive)
        cls._settings_dialog.raise_()


def add_menu_action(
        menu: QMenu,
        *,
        text: str,
        cb: Callable,
        icon: str = None
) -> QAction:
    action = menu.addAction(text)
    if icon:
        action.setIcon(utils.get_icon(icon))
    action.triggered.connect(cb)
    return action


def get_settings_action(
        menu,
        icon: str = None
) -> QAction:
    action = add_menu_action(
        menu=menu,
        icon=icon,
        text="设置",
        cb=lambda: Action.show_settings()
    )

    return action


def get_quit_action(menu, icon: str = None) -> QAction:
    action = add_menu_action(
        menu,
        text="退出",
        icon=icon,
        cb=Action.quit_app
    )
    return action
