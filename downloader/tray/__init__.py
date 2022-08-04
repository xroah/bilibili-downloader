from PySide6.QtWidgets import QApplication, QMainWindow

from .Tray import Tray


tray: Tray | None = None


def create_tray(app: QApplication, win: QMainWindow):
    global tray
    if tray is None:
        tray = Tray(app, win)
    return tray


def get_tray():
    return tray

