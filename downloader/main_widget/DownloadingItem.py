from typing import cast

from PySide6.QtWidgets import (
    QProgressBar,
    QWidget,
    QToolButton,
    QStackedLayout
)
from PySide6.QtCore import QSize
from PySide6.QtGui import (
    QIcon,
    QContextMenuEvent,
    QCursor,
    QMouseEvent
)
from PySide6.QtUiTools import QUiLoader

from ..utils import utils
from ..common_widgets import Menu


class DownloadingItem(QProgressBar):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self.paused = True
        self.bg = QWidget(self)
        self.ctx_menu = Menu(self)
        self.selected = False
        self.ctx_menu.addAction("开始/暂停")
        self.ctx_menu.addAction("打开文件夹")
        self.ctx_menu.addAction("删除")
        self.ctx_menu.addAction("属性")
        self.init_layout()

    def init_layout(self):
        layout = QStackedLayout(self)
        loader = QUiLoader()
        widget = loader.load(utils.get_resource_path("uis/downloading-item.ui"))
        icon = cast(
            QToolButton,
            widget.findChild(QToolButton, "icon")
        )
        toggle_btn = cast(
            QToolButton,
            widget.findChild(QToolButton, "toggle")
        )
        icon.setIcon(utils.get_icon("video"))
        icon.setIconSize(QSize(50, 50))
        toggle_btn.setIcon(QIcon(utils.get_icon("play")))
        toggle_btn.setIconSize(QSize(32, 32))
        self.bg.setObjectName("background")
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(widget)
        layout.addWidget(self.bg)
        layout.setStackingMode(QStackedLayout.StackAll)
        self.setTextVisible(False)
        self.setValue(50)
        self.setProperty("class", "downloading-item")
        self.setStyleSheet(utils.get_style("downloading-item"))

    def contextMenuEvent(self, e: QContextMenuEvent) -> None:
        self.ctx_menu.exec(QCursor.pos())

    def mouseDoubleClickEvent(self, e: QMouseEvent) -> None:
        print("double click")

    def mousePressEvent(self, e: QMouseEvent) -> None:
        print("mouse press")
        self.selected = not self.selected
        if self.selected:
            self.bg.setStyleSheet("""
                background-color: rgba(13, 110, 253, .2);
            """)
        else:
            self.bg.setStyleSheet("")
