from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QToolBar,
    QToolButton,
    QWidget,
    QSizePolicy,
    QMainWindow,
    QPushButton
)

from ..utils import utils
from ..common_widgets import ToolButton
from .NewDialog import NewDialog
from .MainMenu import MainMenu
from .LoginDialog import LoginDialog


class Toolbar(QToolBar):
    def __init__(self, parent: QMainWindow):
        super().__init__(parent)
        self._window = parent
        self.add_btn = ToolButton(self, "plus")
        self.login_btn = QPushButton(parent=self, text="登录Bilibili账号")
        self.menu_btn = ToolButton(self, "menu")
        self.menu = MainMenu(parent, self, self.menu_btn)
        self.add_btn.clicked.connect(self.show_new_dialog)
        self.login_btn.clicked.connect(self.show_login_dialog)
        self.menu_btn.setPopupMode(QToolButton.InstantPopup)
        self.menu_btn.setMenu(self.menu)
        self.init()

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
        LoginDialog(self._window)
