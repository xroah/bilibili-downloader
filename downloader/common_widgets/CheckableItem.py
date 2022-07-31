from typing import cast

from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QStackedLayout
)
from PySide6.QtGui import (
    QMouseEvent,
    QCursor,
    QContextMenuEvent,
    QPixmap
)
from PySide6.QtCore import QSize

from ..common_widgets import Menu


class CheckableItem(QWidget):
    def __init__(
            self,
            *,
            widget: QWidget,
            parent: QWidget = None
    ):
        super().__init__(parent)
        self._bg = QWidget(self)
        self._widget = widget
        self._checked = False
        self._ctx_menu = Menu(self)
        self._widget.setParent(self)
        self.init_layout()

    def init_layout(self):
        layout = QStackedLayout(self)
        icon = cast(
            QLabel,
            self._widget.findChild(QLabel, "icon")
        )
        if icon:
            size = QSize(48, 36)
            pixmap = QPixmap(":/icons/video.svg")
            icon.setFixedSize(size)
            icon.setPixmap(pixmap)
            icon.setStyleSheet("""
                padding: 0;
                border: none;
                background-color: transparent;
            """)
        self._bg.setObjectName("background")
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self._widget)
        layout.addWidget(self._bg)
        layout.setStackingMode(QStackedLayout.StackAll)

    def mousePressEvent(self, e: QMouseEvent) -> None:
        print("mouse press")
        self._checked = not self._checked
        if self._checked:
            self._bg.setStyleSheet("""
                background-color: rgba(13, 110, 253, .3);
            """)
        else:
            self._bg.setStyleSheet("")

    def contextMenuEvent(self, e: QContextMenuEvent) -> None:
        self._ctx_menu.exec(QCursor.pos())
