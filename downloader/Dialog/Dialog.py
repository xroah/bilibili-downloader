from PySide6.QtCore import Qt, QSize, Signal
from PySide6.QtGui import QIcon, QShowEvent
from PySide6.QtWidgets import (
    QDialog,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton
)
from ..CommonWidgets import PushButton, ToolButton
from ..Color import Color


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
        self.setStyleSheet("""
            .header {
                background-color: #16181d;
            }
            
            .header QLabel {
                padding: 5px;
                color: #fff;
            }
            
            .header QToolButton {
                padding: 0;
                margin-right: 5px;
                border: none;
            }
            
            .body {
                background-color: #fff;
            }
       """)

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

        footer.setStyleSheet("""
            QWidget {
                background-color: #f0f0f0;
            }
        
            PushButton, QPushButton {
                width: 60px;
                padding: 8px 5px;
                margin-right: 5px;
                border: none;
            }
            
            .ok {
                margin-left: 5px;
            }
        """)
        ok_btn.setProperty("class", "ok")
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
