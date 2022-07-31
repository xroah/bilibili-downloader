from typing import Callable

from PySide6.QtCore import QSize, Qt, Signal
from PySide6.QtGui import QShowEvent, QGuiApplication
from PySide6.QtWidgets import (
    QDialog,
    QWidget,
    QVBoxLayout,
    QHBoxLayout
)
from . import PushButton
from ..utils import utils


class Dialog(QDialog):
    shown = Signal()

    def __init__(
            self,
            parent: QWidget,
            size: QSize,
            title: str = "",
            is_modal: bool = True,
            content: QWidget = None,
            show_cancel: bool = False,
            show_footer: bool = True,
            close_on_ok: bool = True,
            ok_callback: Callable = None
    ):
        super().__init__(parent)
        self._parent = parent
        self.title = title
        self.content = content
        self.show_cancel = show_cancel
        self.show_footer = show_footer
        self.close_on_ok = close_on_ok
        self.ok_callback = ok_callback
        self.body = self._get_body()
        self.setModal(bool(is_modal))
        self.setWindowTitle(title)
        self.setFixedSize(size)
        self._set_layout()
        self.setAttribute(Qt.WA_DeleteOnClose, True)

    def _set_layout(self):
        layout = QVBoxLayout()
        layout.addWidget(self.body, 1)
        if self.show_footer:
            footer = self._get_footer()
            layout.addWidget(footer)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.setLayout(layout)
        self.setStyleSheet(utils.get_style("dialog"))

    def _get_body(self) -> QWidget:
        body = QWidget(self)
        layout = QVBoxLayout(body)
        body.setProperty("class", "body")

        if self.content:
            layout.addWidget(self.content)

        body.setLayout(layout)

        return body

    def _get_footer(self) -> QWidget:
        footer = QWidget(self)
        layout = QHBoxLayout()
        ok_btn = PushButton(parent=footer, text="确定")

        footer.setProperty("class", "footer")
        ok_btn.clicked.connect(self.ok)
        ok_btn.setProperty("class", "primary")
        layout.addStretch()

        if self.show_cancel:
            cancel_btn = PushButton(parent=footer, text="取消")
            cancel_btn.clicked.connect(self.cancel)
            layout.addWidget(cancel_btn)

        layout.setSpacing(0)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.addWidget(ok_btn)
        footer.setLayout(layout)

        return footer

    def set_content(self, content: QWidget) -> None:
        if content is None or not isinstance(content, QWidget):
            return

        layout = self.body.layout()

        if self.content:
            layout.removeWidget(self.content)
            self.content.deleteLater()

        self.content = content
        content.setParent(self)
        layout.addWidget(content)

    def ok(self):
        if self.close_on_ok:
            self.accept()

        if self.ok_callback:
            self.ok_callback()

    def cancel(self):
        self.reject()

    def showEvent(self, e: QShowEvent) -> None:
        size = self.size()

        if not self.isModal() and not self._parent.isVisible():
            screen = QGuiApplication.primaryScreen()
            avail_size = screen.availableSize()
            left = (avail_size.width() - size.width()) / 2
            top = (avail_size.height() - size.height()) / 2
        else:
            p_geometry = self._parent.frameGeometry()
            left = (p_geometry.width() - size.width()) / 2
            top = (p_geometry.height() - size.height()) / 2
            left += p_geometry.x()
            top += p_geometry.y()

        self.move(left, top)
        self.shown.emit()
