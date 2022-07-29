import os
from typing import cast
import json
from threading import Thread

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QToolBar,
    QToolButton,
    QWidget,
    QSizePolicy,
    QMainWindow,
    QPushButton
)
import httpx

from ..utils import utils
from ..enums import Req
from ..common_widgets import ToolButton
from .NewDialog import NewDialog
from .MainMenu import MainMenu
from .LoginDialog import LoginDialog


class Toolbar(QToolBar):
    login_check_finished = Signal(bool, str)

    def __init__(self, parent: QMainWindow):
        super().__init__(parent)
        self._window = parent
        self.is_login = False
        self.add_btn = ToolButton(self, "plus")
        self.login_btn = QPushButton(parent=self, text="登录Bilibili账号")
        self.menu_btn = ToolButton(self, "menu")
        self.menu = MainMenu(parent, self, self.menu_btn)
        self.add_btn.clicked.connect(self.show_new_dialog)
        self.login_btn.clicked.connect(self.show_login_dialog)
        self.login_check_finished.connect(self.login_checked)
        self.login_btn.setEnabled(False)
        self.menu_btn.setPopupMode(QToolButton.InstantPopup)
        self.menu_btn.setMenu(self.menu)
        self.init()
        self.start_check_login()

    def check_login_state(self):
        def emit_false():
            self.login_check_finished.emit(False)

        data_dir = utils.get_data_dir()
        cookie_text = os.path.join(data_dir, "cookie.txt")
        with open(cookie_text, "r") as f:
            cookie = f.read().strip()

        if not cookie:
            emit_false()
            return
        try:
            res = httpx.get(
                cast(str, Req.CHECK_LOGIN.value),
                headers={
                    "referer": Req.REFERER.value,
                    "user-agent": Req.USER_AGENT.value,
                    "cookie": cookie
                }
            )
            res = json.loads(res.text)
            print(res)
        except Exception:
            emit_false()
        else:
            if res["code"] != 0:
                emit_false()
                return
            data = res["data"]
            self.login_check_finished.emit(
                data["isLogin"],
                data["uname"]
            )

    def start_check_login(self):
        t = Thread(target=self.check_login_state)
        t.daemon = True
        t.start()

    def login_checked(self, is_login: bool, uname: str):
        self.is_login = is_login
        if is_login:
            self.login_btn.setEnabled(True)
            self.login_btn.setText(uname)
            self.login_btn.setToolTip("点击退出")

    def init(self):
        placeholder = QWidget()
        placeholder.setProperty("class", "placeholder")
        placeholder.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.login_btn.setProperty("class", "login-btn")
        self.login_btn.setCursor(Qt.PointingHandCursor)
        self.addWidget(self.add_btn)
        self.addWidget(placeholder)
        self.addWidget(self.login_btn)
        self.addWidget(self.menu_btn)
        self.setContextMenuPolicy(Qt.PreventContextMenu)
        self.setObjectName("toolbar")
        self.setMovable(False)
        self.setStyleSheet(utils.get_style("toolbar"))

    def show_new_dialog(self):
        NewDialog(self._window)

    def show_login_dialog(self):
        if self.is_login:
            return

        dialog = LoginDialog(self._window)
        dialog.login_success.connect(lambda: self.start_check_login)
