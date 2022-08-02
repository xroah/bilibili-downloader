from threading import Thread

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QToolBar,
    QToolButton,
    QWidget,
    QSizePolicy,
    QMainWindow,
    QLabel
)

from ..utils import utils, request, event_bus
from ..Cookie import Cookie
from ..common_widgets import ToolButton, MessageBox
from .NewDialog import NewDialog
from .MainMenu import MainMenu
from ..enums import Req, EventName


class Toolbar(QToolBar):
    login_check_finished = Signal(bool, str)

    def __init__(self, parent: QMainWindow):
        super().__init__(parent)
        self._window = parent
        self.cookie = Cookie()
        self.add_btn = ToolButton(self, "plus")
        self.start_all_btn = ToolButton(self, "play")
        self.pause_all_btn = ToolButton(self, "pause")
        self.default_login_text = "bilibili账号未登录"
        self.user_name = QLabel(self.default_login_text)
        self.menu_btn = ToolButton(self, "menu")
        self.menu = MainMenu(parent, self, self.menu_btn)
        self.add_btn.setToolTip("新建下载")
        self.start_all_btn.setToolTip("全部开始")
        self.pause_all_btn.setToolTip("全部暂停")
        self.menu_btn.setToolTip("菜单")
        self.menu_btn.setPopupMode(QToolButton.InstantPopup)
        self.menu_btn.setMenu(self.menu)
        self.init()
        self.start_check_login()

        self.add_btn.clicked.connect(self.show_new_dialog)
        self.login_check_finished.connect(self.login_checked)
        event_bus.on(EventName.COOKIE_CHANGE, self.check_login_state)

    def check_login_state(self):
        def emit_false():
            self.login_check_finished.emit(False, "")

        if not self.cookie.cookie:
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
            self.login_check_finished.emit(
                data["isLogin"],
                data["uname"]
            )

    def start_check_login(self):
        t = Thread(target=self.check_login_state)
        t.daemon = True
        t.start()

    def login_checked(self, is_login: bool, uname: str):
        if is_login:
            self.user_name.setText(uname)
        elif self.cookie.cookie:
            MessageBox.alert("登录已过期, 请重新登录", parent=self._window)
        else:
            self.user_name.setText(self.default_login_text)

    def init(self):
        placeholder = QWidget()
        placeholder.setProperty("class", "placeholder")
        placeholder.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.user_name.setProperty("class", "user-name")
        self.addWidget(self.add_btn)
        self.addWidget(self.start_all_btn)
        self.addWidget(self.pause_all_btn)
        self.addWidget(placeholder)
        self.addWidget(self.user_name)
        self.addWidget(self.menu_btn)
        self.setContextMenuPolicy(Qt.PreventContextMenu)
        self.setObjectName("toolbar")
        self.setMovable(False)
        self.setStyleSheet(utils.get_style("toolbar"))

    def show_new_dialog(self):
        NewDialog(self._window)
