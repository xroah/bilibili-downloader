import sys

from PySide6.QtGui import QCursor
from PySide6.QtWidgets import (
    QApplication,
    QSystemTrayIcon,
    QMenu
)

from .MainWindow import MainWindow
from .utils import utils


class App(QApplication):
    def __init__(self):
        super().__init__()
        tray_avail = QSystemTrayIcon.isSystemTrayAvailable()
        self.tray = QSystemTrayIcon()
        self.main_win = MainWindow(tray_avail)

        if tray_avail:
            self.init_tray()

    def init_tray(self):
        tray = self.tray
        tray.setIcon(utils.get_icon("logo"))
        tray.show()
        tray.setToolTip("Bilibli下载器")
        tray.setContextMenu(self.get_ctx_menu())
        tray.activated.connect(self.tray_activated)

    def tray_activated(self, reason):
        match reason:
            case QSystemTrayIcon.Trigger:
                self.show_win()
            case QSystemTrayIcon.Context:
                ctx_menu = self.tray.contextMenu()
                ctx_menu.exec(QCursor.pos())
            case _:
                pass

    def show_win(self):
        win = self.main_win

        if not win.isVisible():
            win.show()
        elif win.isMinimized():
            win.showNormal()

        win.activateWindow()

    def get_ctx_menu(self) -> QMenu:
        menu = QMenu(self.main_win)
        show_main_action = menu.addAction("显示主界面")
        exit_action = menu.addAction("退出")
        show_main_action.triggered.connect(self.show_win)
        exit_action.triggered.connect(lambda: sys.exit(0))
        menu.setProperty("class", "contextmenu")
        menu.setStyleSheet(utils.get_style("menu"))

        return menu
