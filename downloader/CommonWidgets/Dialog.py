from PySide6.QtCore import QSize
from PySide6.QtGui import QShowEvent
from PySide6.QtWidgets import (
    QDialog,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
)
from . import PushButton
from ..utils import utils


class Dialog(QDialog):
    def __init__(
            self,
            parent: QWidget,
            size: QSize,
            title: str = "",
            content: QWidget = None,
            show_cancel: bool = False
    ):
        super().__init__(parent)
        self._parent = parent
        self.title = title
        self.content = content
        self.show_cancel = show_cancel
        self.body = self._get_body()
        self.setWindowTitle(title)
        self.setModal(True)
        self.setFixedSize(size)
        self._set_layout()

    def open(self):
        super().open()

    def _set_layout(self):
        layout = QVBoxLayout(self)
        footer = self._get_footer()
        layout.addWidget(self.body, 1)
        layout.addWidget(footer)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.setLayout(layout)

        with open(utils.get_resource_path("styles/dialog.qss")) as ss:
            self.setStyleSheet(ss.read())

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
        layout = QHBoxLayout(footer)
        ok_btn = PushButton(parent=footer, text="确定")

        footer.setProperty("class", "footer")
        ok_btn.clicked.connect(self._ok)
        layout.addStretch()

        if self.show_cancel:
            cancel_btn = PushButton(
                parent=footer,
                text="取消",
                primary=False
            )
            cancel_btn.setProperty("class", "cancel")
            cancel_btn.clicked.connect(self._cancel)
            layout.addWidget(cancel_btn)

        layout.setSpacing(0)
        layout.setContentsMargins(5, 5, 5, 5)
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
        layout.addWidget(content)

    def _ok(self):
        self.accept()

    def _cancel(self):
        self.reject()

    def showEvent(self, e: QShowEvent) -> None:
        super().showEvent(e)
        p_geometry = self._parent.frameGeometry()
        size = self.size()
        left = (p_geometry.width() - size.width()) / 2
        top = (p_geometry.height() - size.height()) / 2

        self.move(p_geometry.x() + left, p_geometry.y() + top)
