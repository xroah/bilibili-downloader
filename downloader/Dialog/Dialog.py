from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QShowEvent
from PySide6.QtWidgets import (
    QDialog,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
)
from ..CommonWidgets import PushButton, ToolButton
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
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setModal(True)
        self.setFixedSize(size)
        self._set_layout()

    def open(self):
        super().open()

    def _set_layout(self):
        v_box_layout = QVBoxLayout(self)
        header = self._get_header()
        footer = self._get_footer()
        v_box_layout.addWidget(header)
        v_box_layout.addWidget(self.body, 1)
        v_box_layout.addWidget(footer)
        v_box_layout.setContentsMargins(0, 0, 0, 0)
        v_box_layout.setSpacing(0)
        self.setLayout(v_box_layout)

        with open(utils.get_resource_path("styles/dialog.qss")) as ss:
            self.setStyleSheet(ss.read())

    def _get_header(self) -> QWidget:
        header = QWidget(self)
        title = QLabel(self.title)
        close_btn = ToolButton(header, ":/close.png")
        layout = QHBoxLayout(header)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(title)
        close_btn.setIconSize(QSize(24, 24))
        close_btn.clicked.connect(self._cancel)

        layout.addWidget(close_btn)
        header.setLayout(layout)
        header.setProperty("class", "header")

        return header

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
            cancel_btn = PushButton(parent=footer, text="取消", primary=False)
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
        p_geometry = self._parent.frameGeometry()
        size = self.size()
        left = (p_geometry.width() - size.width()) / 2
        top = (p_geometry.height() - size.height()) / 2

        self.move(p_geometry.x() + left, p_geometry.y() + top)
