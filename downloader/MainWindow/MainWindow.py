from PySide6.QtCore import QSize, Qt, __version__
from PySide6.QtGui import QIcon, QMoveEvent, QAction
from PySide6.QtWidgets import (
    QMainWindow,
    QToolBar,
    QToolButton,
    QWidget,
    QSizePolicy,
    QMenu,
    QLabel,
    QVBoxLayout
)
import sys
from typing import Callable

from ..MainWidget import MainWidget
from ..utils import utils
from ..Dialog import Dialog
from ..Color import Color
from ..CommonWidgets import ToolButton, PushButton
import __main__


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.add_btn = ToolButton(self, ":/plus.png")
        self.menu_btn = ToolButton(self, ":/menu.png")
        self.menu = QMenu(self)
        self.setCentralWidget(MainWidget())
        self.setWindowTitle("Bilibili下载器")
        self.setMinimumSize(QSize(1080, 720))
        self.setWindowIcon(QIcon(":/logo.png"))
        self.menu_btn.setCursor(Qt.PointingHandCursor)
        self.set_menu(self.menu_btn)
        self.set_toolbar()
        self.show()

    def set_menu(self, btn: QToolButton):
        qss_text = """
            QMenu {
                padding: 0;
                border-radius: 5px;
                border: 1px solid #f0f0f0; 
                background-color: #fff;
            }
            
            QMenu::item {
                margin: 0;
                width: 150px;
                padding: 10px;
            }
            
            QMenu::item:selected {
                color: #fff;
                hover_color;
            }
        """.replace("hover_color", Color.BUTTON_HOVER.value)
        self.add_action("关于", self.about_action)
        self.add_action("退出", lambda: sys.exit(0))
        btn.setPopupMode(QToolButton.InstantPopup)
        btn.setMenu(self.menu)
        self.menu.setStyleSheet(qss_text)

    def add_action(
            self,
            text: str,
            cb: Callable[[bool], None]
    ) -> QAction:
        action = self.menu.addAction(text)

        if cb is not None:
            action.triggered.connect(cb)

        return action

    def about_action(self):
        dialog = Dialog(
            self,
            QSize(260, 200),
            "关于",
            QLabel("dddd"),
            True
        )
        filename = utils.get_resource_path("resources/about.html")

        with open(filename, "r", encoding="utf-8") as f:
            text = f.read().format(v=__main__.__version__, pv=__version__)

        w = QWidget(dialog.body)
        about = QLabel()
        layout = QVBoxLayout(w)
        about.setText(text)
        about.setOpenExternalLinks(True)
        layout.addWidget(about)
        w.setLayout(layout)

        dialog.set_content(w)
        dialog.open()

    def set_toolbar(self):
        toolbar = QToolBar(self)
        toolbar.setMovable(False)
        placeholder = QWidget()
        placeholder.setProperty("class", "placeholder")
        placeholder.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        toolbar.setObjectName("toolbar")
        toolbar.addWidget(self.add_btn)
        toolbar.addWidget(placeholder)
        toolbar.addWidget(self.menu_btn)
        toolbar.setContextMenuPolicy(Qt.PreventContextMenu)

        with open(utils.get_resource_path("styles/toolbar.qss")) as ss:
            toolbar.setStyleSheet(ss.read())

        self.addToolBar(toolbar)

    def moveEvent(self, event: QMoveEvent) -> None:
        pos = event.pos()
        print(pos)
