import os
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

from ..utils import utils
from ..utils import request
from ..cookie import Cookie
from ..enums import Req
from ..common_widgets import ToolButton, MessageBox
from .NewDialog import NewDialog
from .MainMenu import MainMenu
from .LoginDialog import LoginDialog


class Toolbar(QToolBar):
    login_check_finished = Signal(bool, str)

    def __init__(self, parent: QMainWindow):
        super().__init__(parent)
        self._window = parent
        self.is_login = False
        self.cookie = Cookie()
        self.add_btn = ToolButton(self, "plus")
        self.login_btn = QPushButton(parent=self, text="登录Bilibili账号")
        self.menu_btn = ToolButton(self, "menu")
        self.menu = MainMenu(parent, self, self.menu_btn)
        self.add_btn.clicked.connect(self.show_new_dialog)
        self.login_btn.clicked.connect(self.login_out)
        self.login_check_finished.connect(self.login_checked)
        self.login_btn.setEnabled(False)
        self.menu_btn.setPopupMode(QToolButton.InstantPopup)
        self.menu_btn.setMenu(self.menu)
        self.init()
        self.start_check_login()

    def check_login_state(self):
        def emit_false():
            self.login_check_finished.emit(False, "")

        if not self.cookie.cookie:
            emit_false()
            return

        try:
            res = request.get(str(Req.CHECK_LOGIN))
            res = json.loads(res.text)
        except:
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
        self.login_btn.setEnabled(True)
        if is_login:
            self.login_btn.setText(uname)
            self.login_btn.setToolTip("点击退出")
        elif self.cookie.cookie:
            MessageBox.alert("登录已过期, 请重新登录")
            self.cookie.delete()

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
        dialog = LoginDialog(self._window)
        dialog.login_success.connect(lambda: self.start_check_login)

    def logout(self):
        data_dir = utils.get_data_dir()
        cookie_file = os.path.join(data_dir, "cookie")

    def login_out(self):
        if self.is_login:
            MessageBox.confirm(
                "确定要退出登录吗?",
                on_ok=self.logout
            )
            return

        self.show_login_dialog()
