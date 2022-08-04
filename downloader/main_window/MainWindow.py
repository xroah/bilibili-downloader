import sys
import os.path
from typing import cast, TypeVar, Generic
from threading import Thread

from PySide6.QtCore import QSize, Qt, Signal
from PySide6.QtGui import (
    QCloseEvent,
    QKeyEvent,
    QResizeEvent,
    QImage,
    QPixmap
)
from PySide6.QtWidgets import (
    QMainWindow,
    QSystemTrayIcon,
    QWidget,
    QStackedLayout,
    QLabel,
    QGraphicsBlurEffect,
    QToolButton,
    QPushButton,
    QStackedWidget
)
from PySide6.QtUiTools import QUiLoader

from ..utils import (
    utils,
    event_bus,
    decorators,
    request
)
from ..enums import EventName, Req
from .MainMenu import MainMenu
from .NewDialog import NewDialog
from ..main_widget import DownloadingPanel, DownloadedPanel
from ..common_widgets import MessageBox
from ..cookie import cookie

T = TypeVar("T", bound='QWidget')


@decorators.singleton
class MainWindow(QMainWindow):
    bg_sig = Signal(str)
    login_sig = Signal(bool, str)

    def __init__(self):
        super().__init__()
        loader = QUiLoader()
        central_widget = QWidget(self)
        widget = loader.load(utils.get_resource_path("uis/main.ui"))
        self.default_login_state = "bilibili帐号未登录"
        self.hide_to_tray = QSystemTrayIcon.isSystemTrayAvailable()
        self.bg = utils.get_resource_path("default-bg.png")
        self._size = QSize(900, 580)
        self.menu_btn = utils.get_child(widget, QToolButton, "menu")
        self.new_btn = utils.get_child(widget, QToolButton, "newDownload")
        self.start_all = utils.get_child(widget, QToolButton, "startAll")
        self.pause_all = utils.get_child(widget, QToolButton, "pauseAll")
        self.new_btn.setIcon(utils.get_icon("plus"))
        self.menu_btn.setIcon(utils.get_icon("menu"))
        self.start_all.setIcon(utils.get_icon("play"))
        self.pause_all.setIcon(utils.get_icon("pause"))
        self.bg_label = QLabel(central_widget)
        self.username = utils.get_child(widget, QLabel, "username")
        self.menu = MainMenu(self, self.menu_btn)
        self.downloading_tab = utils.get_child(
            widget,
            QPushButton,
            "downloading"
        )
        self.downloaded_tab = utils.get_child(
            widget,
            QPushButton,
            "downloaded"
        )
        self.current_tab: QPushButton | None = None
        self.right_panel = cast(
            QStackedWidget,
            widget.findChild(QStackedWidget, "rightPanel")
        )
        self.right_panel.addWidget(DownloadingPanel(self))
        self.right_panel.addWidget(DownloadedPanel(self))
        widget.setParent(central_widget)
        central_layout = QStackedLayout(central_widget)
        central_layout.setStackingMode(QStackedLayout.StackAll)
        central_layout.addWidget(self.bg_label)
        central_layout.addWidget(widget)
        central_layout.setCurrentIndex(1)
        central_widget.setLayout(central_layout)

        self.init(central_widget)
        self.init_signal()

    def init(self, central: QWidget):
        central.setStyleSheet(utils.get_style("main", "toolbutton"))
        self.username.setText(self.default_login_state)
        self.menu_btn.setPopupMode(QToolButton.InstantPopup)
        self.menu_btn.setMenu(self.menu)
        self.setCentralWidget(central)
        self.setWindowTitle("Bilibili下载器")
        self.setMinimumSize(self._size)
        self.setWindowIcon(utils.get_icon("logo", "png"))
        self.setWindowFlags(
            Qt.CustomizeWindowHint |
            Qt.WindowCloseButtonHint |
            Qt.WindowMaximizeButtonHint |
            Qt.WindowMinimizeButtonHint
        )
        self.set_bg_img()
        self.switch_tab(self.downloading_tab)
        self.start_check_login()
        self.show()

    def init_signal(self):
        event_bus.on(EventName.NEW_DOWNLOAD, lambda d: print(d))
        event_bus.on(EventName.COOKIE_CHANGE, self.start_check_login)
        self.bg_sig.connect(self.set_bg_img)
        self.new_btn.clicked.connect(lambda: NewDialog(self))
        self.downloading_tab.clicked.connect(
            lambda: self.switch_tab(self.downloading_tab)
        )
        self.downloaded_tab.clicked.connect(
            lambda: self.switch_tab(self.downloaded_tab)
        )
        self.login_sig.connect(self.login_checked)

    def set_bg_img(self, bg: str = ""):
        if bg:
            self.bg = bg

        if not self.bg or not os.path.exists(self.bg):
            return

        img = QImage(self.bg)
        img = img.scaled(self.size())
        blur_effect = QGraphicsBlurEffect(self.bg_label)
        blur_effect.setBlurRadius(10)
        self.bg_label.setPixmap(QPixmap.fromImage(img))
        self.bg_label.setGraphicsEffect(blur_effect)

    def switch_tab(self, btn: QPushButton):
        if self.current_tab:
            if self.current_tab == btn:
                return

            self.current_tab.setStyleSheet("")

        self.current_tab = btn
        tab = btn.property("tab")
        self.right_panel.setCurrentIndex(tab)
        btn.setStyleSheet(utils.get_style("active"))

    def show(self) -> None:
        self.resize(self._size)
        super().show()

    def check_login_state(self):
        def emit_false():
            self.login_sig.emit(False, "")

        if not cookie.cookie:
            emit_false()
            return

        try:
            res = request.get(str(Req.CHECK_LOGIN))
            res = res.json()
        except:
            pass
        else:
            if res["code"] != 0:
                emit_false()
                return
            data = res["data"]
            self.login_sig.emit(
                data["isLogin"],
                data["uname"]
            )

    def start_check_login(self):
        t = Thread(target=self.check_login_state)
        t.daemon = True
        t.start()

    def login_checked(self, is_login: bool, uname: str):
        if is_login:
            self.username.setText(uname)
        elif cookie.cookie:
            MessageBox.alert(
                "登录已过期或者cookie设置错误",
                parent=self
            )
        else:
            self.username.setText(self.default_login_state)

    def closeEvent(self, e: QCloseEvent) -> None:
        if self.hide_to_tray:
            self.hide()
            e.ignore()
        else:
            e.accept()

    def keyPressEvent(self, e: QKeyEvent) -> None:
        combination = e.keyCombination()
        # mac os hot key
        if (
                sys.platform == "darwin" and
                combination.keyboardModifiers() == Qt.MetaModifier
        ):
            match e.key():
                case Qt.Key_W:
                    self.close()
                case Qt.Key_M:
                    self.showMinimized()

    def resizeEvent(self, e: QResizeEvent) -> None:
        self._size = e.size()
        self.set_bg_img()
