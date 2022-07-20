from PySide6.QtCore import Qt, __version__
from PySide6.QtWidgets import (
    QToolBar,
    QToolButton,
    QWidget,
    QSizePolicy,
    QMainWindow
)

from ..utils import utils
from ..CommonWidgets import ToolButton
from .NewDialog import NewDialog
from .Menu import Menu


class Toolbar(QToolBar):
    def __init__(self, parent: QMainWindow):
        super().__init__(parent)
        self._window = parent
        self.add_btn = ToolButton(self, "plus")
        self.menu_btn = ToolButton(self, "menu")
        self.menu = Menu(parent, self, self.menu_btn)
        self.add_btn.clicked.connect(self.show_new_dialog)
        self.menu_btn.setPopupMode(QToolButton.InstantPopup)
        self.menu_btn.setMenu(self.menu)
        self.init()

    def init(self):
        placeholder = QWidget()
        placeholder.setProperty("class", "placeholder")
        placeholder.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.addWidget(self.add_btn)
        self.addWidget(placeholder)
        self.addWidget(self.menu_btn)
        self.setContextMenuPolicy(Qt.PreventContextMenu)
        self.setObjectName("toolbar")
        self.setMovable(False)

        with open(utils.get_resource_path("styles/toolbar.qss")) as ss:
            self.setStyleSheet(ss.read())

    def show_new_dialog(self):
        dialog = NewDialog(self._window)
        dialog.open()