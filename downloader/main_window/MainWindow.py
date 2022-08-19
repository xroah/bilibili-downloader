import sys
import os.path
from typing import cast, TypeVar
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
from ..main_widget import DownloadingTab, DownloadedTab
from ..common_widgets import MessageBox
from ..cookie import cookie
from .DownloadManager import DownloadManager

T = TypeVar("T", bound='QWidget')
downloading_text = "正在下载"
downloaded_text = "已下载"


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
        toolbar = utils.get_child(widget, QWidget, "toolbar")
        self.menu_btn = utils.get_child(widget, QToolButton, "menu")
        self.new_btn = utils.get_child(widget, QToolButton, "newDownload")
        self.start_all_btn = utils.get_child(widget, QToolButton, "startAll")
        self.pause_all_btn = utils.get_child(widget, QToolButton, "pauseAll")
        self.new_btn.setIcon(utils.get_icon("plus"))
        self.menu_btn.setIcon(utils.get_icon("menu"))
        self.start_all_btn.setIcon(utils.get_icon("play"))
        self.pause_all_btn.setIcon(utils.get_icon("pause"))
        self.bg_label = QLabel(central_widget)
        self.username = utils.get_child(widget, QLabel, "username")
        self.menu = MainMenu(self, self.menu_btn)
        self.current_tab: QPushButton | None = None
        self.downloading_btn = utils.get_child(
            widget,
            QPushButton,
            "downloading"
        )
        self.downloaded_btn = utils.get_child(
            widget,
            QPushButton,
            "downloaded"
        )
        self.right_panel = utils.get_child(
            widget,
            QStackedWidget,
            "rightPanel"
        )
        downloading_tab = DownloadingTab(self)
        downloaded_tab = DownloadedTab(self)
        self.dm = DownloadManager(
            window=self,
            downloaded_tab=downloaded_tab,
            downloading_tab=downloading_tab
        )
        toolbar.setFixedHeight(50)
        self.downloading_btn.setFixedWidth(150)
        self.downloaded_btn.setFixedWidth(150)
        self.right_panel.addWidget(downloading_tab)
        self.right_panel.addWidget(downloaded_tab)
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
        self.switch_tab(self.downloading_btn)
        self.start_check_login()
        # self.show()

    def init_signal(self):
        event_bus.on(EventName.COOKIE_CHANGE, self.start_check_login)
        self.bg_sig.connect(self.set_bg_img)
        self.new_btn.clicked.connect(lambda: NewDialog(self))
        self.downloading_btn.clicked.connect(
            lambda: self.switch_tab(self.downloading_btn)
        )
        self.downloaded_btn.clicked.connect(
            lambda: self.switch_tab(self.downloaded_btn)
        )
        self.login_sig.connect(self.login_checked)
        self.start_all_btn.clicked.connect(self.dm.start_all)
        self.pause_all_btn.clicked.connect(self.dm.pause_all)
        self.dm.change_sig.connect(self.update_text)

    def set_bg_img(self, bg: str = ""):
        if bg:
            self.bg = bg

        if not self.bg or not os.path.exists(self.bg):
            return

        img = QImage(self.bg)
        img = img.scaled(self.size())
        blur_effect = QGraphicsBlurEffect(self.bg_label)
        blur_effect.setBlurRadius(30)
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
        btn.setStyleSheet("""
            background-color: rgba(0, 174, 236, .8);
            color: #fff;
        """)

        # 已下载tab
        self.pause_all_btn.setEnabled(tab != 1)
        self.start_all_btn.setEnabled(tab != 1)

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

    def update_text(self, d: dict):
        self.downloading_btn.setText(
            f'{downloading_text}({d["downloading"]})'
        )
        self.downloaded_btn.setText(
            f'{downloaded_text}({d["downloaded"]})'
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
        is_mac = sys.platform == "darwin"
        current = self.right_panel.currentWidget()

        # Control key mapped to MetaModifier macos
        if e.modifiers() == Qt.ControlModifier:
            match e.key():
                case Qt.Key_W:
                    if is_mac:
                        self.hide()
                case Qt.Key_M:
                    if is_mac:
                        self.showMinimized()
                case Qt.Key_N:
                    NewDialog(self)
                case Qt.Key_A:
                    current.check_all()
        else:
            match e.key():
                case Qt.Key_Escape:
                    current.uncheck_all()
                case Qt.Key_Delete:
                    print("delete")

    def resizeEvent(self, e: QResizeEvent) -> None:
        self._size = e.size()
        self.set_bg_img()
