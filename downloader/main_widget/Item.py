from typing import cast

from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout
)
from PySide6.QtGui import (
    QCursor,
    QContextMenuEvent,
    QPixmap
)
from PySide6.QtCore import QSize, Qt, QEvent
from PySide6.QtUiTools import QUiLoader

from ..common_widgets import Menu, ClickableWidget
from ..utils import utils


class Item(ClickableWidget):
    def __init__(
            self,
            *,
            parent: any = None,
            ui: str,
            class_name: str
    ):
        loader = QUiLoader()
        widget = loader.load(utils.get_resource_path(f"uis/{ui}.ui"))
        super().__init__(parent)
        self._parent = parent
        self._widget = widget
        self.checked = False
        self._ctx_menu = Menu(self)
        self._widget.setParent(self)
        self.setProperty("class", class_name)
        self.init_layout()
        self.setStyleSheet(utils.get_style("item"))

    def delete(self):
        self._parent.del_sig.emit(self)

    def set_parent(self, parent: QWidget):
        self._parent = parent
        super().setParent(parent)

    def init_layout(self):
        layout = QVBoxLayout()
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
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self._widget)
        self.setLayout(layout)

    def check(self):
        self.checked = True
        self.set_style_sheet(.5)

    def set_style_sheet(self, opacity: float):
        self._widget.setStyleSheet("""
            .item {
                background-color: rgba(0, 174, 236, %s);
            }
        """ % opacity)

    def remove_style_sheet(self):
        self._widget.setStyleSheet("")

    def uncheck(self):
        if not self.checked:
            return

        self.checked = False
        self.remove_style_sheet()

    def click_event(self, modifier: Qt.KeyboardModifiers):
        ctrl_pressed = Qt.ControlModifier == modifier

        if not ctrl_pressed:
            self.uncheck_all()
        if not self.checked:
            self.check()

    def uncheck_all(self):
        self._parent.uncheck_all()

    def contextMenuEvent(self, e: QContextMenuEvent) -> None:
        if not self.checked:
            self.uncheck_all()
            self.check()

        self._ctx_menu.exec(QCursor.pos())

    def enterEvent(self, e: QEvent):
        super().enterEvent(e)

        if not self.checked:
            self.set_style_sheet(.3)

    def leaveEvent(self, e: QEvent):
        super().leaveEvent(e)

        if not self.checked:
            self.remove_style_sheet()