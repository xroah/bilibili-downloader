import sys

from PySide6.QtWidgets import (
    QApplication,
    QSystemTrayIcon,
    QMenu,
    QMainWindow
)

from ..enums import EventName
from ..utils import utils, decorators, event_bus
from ..actions import get_settings_action, get_quit_action


@decorators.singleton
class Tray(QSystemTrayIcon):
    def __init__(
            self,
            app: QApplication = None,
            win: QMainWindow = None
    ):
        super().__init__(app)
        self._window = win
        self.menu_visible = False
        self.current = ""
        self.setIcon(utils.get_icon("logo", "png"))
        self.setToolTip("bilibli下载器")
        self.setContextMenu(self.get_ctx_menu())
        self.show()
        self.messageClicked.connect(self.msg_clicked)

        event_bus.on(EventName.DOWNLOAD_FINISHED, self.show_finish_msg)

    def get_ctx_menu(self) -> QMenu:
        menu = QMenu(self._window)
        show_main_action = menu.addAction("显示主界面")
        get_settings_action(menu)
        get_quit_action(menu)
        menu.setProperty("class", "contextmenu")
        menu.setStyleSheet(utils.get_style("menu"))
        menu.aboutToShow.connect(self._menu_show)
        menu.aboutToHide.connect(self._menu_hide)
        show_main_action.triggered.connect(self.show_win)
        self.activated.connect(self._tray_activated)

        return menu

    def _menu_show(self):
        self.menu_visible = True

    def _menu_hide(self):
        self.menu_visible = False

    def _tray_activated(self, reason):
        if (
                # click
                reason == QSystemTrayIcon.Trigger and
                # macos will show contextmenu on click
                sys.platform != "darwin"
        ):
            self.show_win()

    def show_finish_msg(self, name, path):
        self.current = path

        self.showMessage(
            "下载完成:" + name,
            path,
            QSystemTrayIcon.Information,
            3000
        )

    def msg_clicked(self):
        if self.current:
            utils.open_path(self.current)

    def show_win(self):
        win = self._window

        if not win.isVisible():
            if win.isMaximized():
                win.showMaximized()
            else:
                win.showNormal()
        else:
            # The window is minimized is also visible
            if win.isMinimized():
                if win.isMaximized():
                    win.showMaximized()
                else:
                    win.showNormal()

        win.activateWindow()
        win.raise_()
