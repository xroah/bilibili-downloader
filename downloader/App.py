import sys

from PySide6.QtWidgets import (
    QApplication,
    QSystemTrayIcon,
    QMenu
)
from PySide6.QtCore import Qt

from .MainWindow import MainWindow, SettingsDialog
from .utils import utils


class App(QApplication):
    def __init__(self):
        super().__init__()
        tray_avail = QSystemTrayIcon.isSystemTrayAvailable()
        self.tray = QSystemTrayIcon()
        self.main_win = MainWindow(tray_avail)
        # Keyboard shortcuts on macOS are typically based on the Command
        # (or Cmd) keyboard modifier, represented by the ⌘ symbol.
        # For example, the ‘Copy’ action is Command+C (⌘+C).
        # To ease cross platform development Qt will
        # by default remap Command to the ControlModifier ,
        # to align with other platforms.
        # This allows creating keyboard shortcuts such as “Ctrl+J”,
        # which on macOS will then map to Command+J,
        # as expected by macOS users. The actual Control (or Ctrl)
        # modifier on macOS, represented by ⌃,
        # is mapped to MetaModifier .
        self.setAttribute(Qt.AA_MacDontSwapCtrlAndMeta, True)
        self.applicationStateChanged.connect(self.state_change)

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
        if (
            reason == QSystemTrayIcon.Trigger and
            # mac os will show contextmenu on click
            sys.platform != "darwin"
        ):
            self.show_win()

    def show_win(self):
        win = self.main_win

        if not win.isVisible():
            win.show()
        elif win.isMinimized():
            win.showNormal()

        win.activateWindow()
        win.raise_()

    def get_ctx_menu(self) -> QMenu:
        menu = QMenu(self.main_win)
        show_main_action = menu.addAction("显示主界面")
        settings_action = menu.addAction("设置")
        exit_action = menu.addAction("退出")
        show_main_action.triggered.connect(self.show_win)
        settings_action.triggered.connect(
            lambda: SettingsDialog.create_settings_dialog(self.main_win)
        )
        exit_action.triggered.connect(lambda: sys.exit(0))
        menu.setProperty("class", "contextmenu")
        menu.setStyleSheet(utils.get_style("menu"))

        return menu

    def state_change(self, state):
        if (
            state == Qt.ApplicationActive and
            not self.main_win.isVisible() and
            # macos: if the window is hidden,
            # it will not show when click dock icon,
            # but the app state will be active
            # windows: tray right click will activate the app, just ignore
            sys.platform == "darwin"
        ):
            self.show_win()
