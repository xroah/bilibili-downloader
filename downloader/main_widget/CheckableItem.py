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
from PySide6.QtCore import QSize, Qt, QEvent

from ..common_widgets import Menu, ClickableWidget


class CheckableItem(ClickableWidget):
    def __init__(
            self,
            *,
            widget: QWidget,
            parent: any = None
    ):
        super().__init__(parent)
        self._parent = parent
        self._bg = QWidget(self)
        self._widget = widget
        self.checked = False
        self._ctx_menu = Menu(self)
        self._widget.setParent(self)
        self.init_layout()

    def delete(self):
        self._parent.del_sig.emit(self)

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
                background-color: rgba(0, 174, 236, .5);
        """)

    def uncheck(self):
        self.checked = False
        self._bg.setStyleSheet("")

    def click_event(self, modifier: Qt.KeyboardModifiers):
        ctrl_pressed = Qt.ControlModifier == modifier

        if not ctrl_pressed:
            self.uncheck_all()
        if not self.checked:
            self.check()

    def uncheck_all(self):
        self._parent.uncheck_all()

    def set_enter_style(self):
        if not self.checked:
            self._bg.setStyleSheet("""
                background-color: rgba(0, 174, 236, .3);
            """)

    def contextMenuEvent(self, e: QContextMenuEvent) -> None:
        if not self.checked:
            self.uncheck_all()
            self.check()

        self._ctx_menu.exec(QCursor.pos())

    def enterEvent(self, e: QEvent):
        super().enterEvent(e)

        if not self.checked:
            self._bg.setStyleSheet("""
                background-color: rgba(0, 174, 236, .3);
            """)

    def leaveEvent(self, e: QEvent):
        super().leaveEvent(e)

        if not self.checked:
            self._bg.setStyleSheet("")
