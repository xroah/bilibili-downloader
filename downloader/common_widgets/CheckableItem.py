from typing import cast

from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QStackedLayout
)
from PySide6.QtGui import (
    QCursor,
    QContextMenuEvent,
    QPixmap
)
from PySide6.QtCore import QSize, Qt

from ..common_widgets import Menu
from .ClickableWidget import ClickableWidget


class CheckableItem(ClickableWidget):
    def __init__(
            self,
            *,
            widget: QWidget,
            parent: QWidget = None
    ):
        super().__init__(parent)
        self._parent = parent
        self._bg = QWidget(self)
        self._widget = widget
        self.checked = False
        self._ctx_menu = Menu(self)
        self._widget.setParent(self)
        self.init_layout()

    def set_parent(self, parent: QWidget):
        self._parent = parent
        super().setParent(parent)

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

    def check(self):
        self.checked = True
        self._bg.setStyleSheet("""
                background-color: rgba(0, 174, 236, .36);
        """)

    def uncheck(self):
        self.checked = False
        self._bg.setStyleSheet("")

    def clickEvent(self, modifier: Qt.KeyboardModifiers):
        ctrl_pressed = Qt.ControlModifier == modifier

        if not ctrl_pressed:
            self.uncheck_all()
        if not self.checked:
            self.check()

    def dblClickEvent(self):
        print("dbl click")

    def uncheck_all(self):
        try:
            self._parent.uncheck_all()
        except AttributeError:
            pass

    def contextMenuEvent(self, e: QContextMenuEvent) -> None:
        if not self.checked:
            self.uncheck_all()

        self._ctx_menu.exec(QCursor.pos())
