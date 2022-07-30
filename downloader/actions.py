from typing import Callable
import sys

from PySide6.QtWidgets import QMenu, QMainWindow
from PySide6.QtGui import QAction

from .settings import SettingsDialog
from .utils import utils


class Action:
    _settings_dialog: SettingsDialog | None = None

    @staticmethod
    def quit_app():
        sys.exit(0)

    @classmethod
    def _dialog_close(cls):
        cls._settings_dialog = None

    @classmethod
    def show_settings(cls, win: QMainWindow):
        if cls._settings_dialog is not None:
            cls._settings_dialog.activateWindow()
            cls._settings_dialog.raise_()
            return

        cls._settings_dialog = SettingsDialog(win, cls._dialog_close)


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
        window: QMainWindow,
        icon: str = None
) -> QAction:
    action = add_menu_action(
        menu=menu,
        icon=icon,
        text="设置",
        cb=lambda: Action.show_settings(window)
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
