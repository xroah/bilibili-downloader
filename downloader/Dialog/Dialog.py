from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QDialog,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QToolButton,
)


class Dialog(QDialog):
    def __init__(
            self,
            parent: QWidget,
            size: QSize,
            title: str = "",
            content: QWidget = None
    ):
        super().__init__(parent)
        self._parent = parent
        self.title = title
        self.content = content
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setModal(True)
        self.setFixedSize(size)
        self.setAttribute(Qt.WA_StyledBackground)
        self.set_layout()

    def show_dialog(self):
        p_size = self._parent.size()
        size = self.size()
        self.setGeometry(
            (p_size.width() - size.width()) / 2,
            (p_size.height() - size.height()) / 2,
            size.width(),
            size.height()
        )

        self.open()

    def set_layout(self):
        v_box_layout = QVBoxLayout(self)
        header = QWidget(self)
        close_btn = QToolButton(header)
        content = QWidget(self)
        header_layout = QHBoxLayout(header)
        title = QLabel(self.title)
        v_box_layout.addWidget(header)
        v_box_layout.addWidget(content, 1)
        v_box_layout.setContentsMargins(5, 5, 5, 5)
        v_box_layout.setSpacing(0)
        self.setLayout(v_box_layout)
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.addWidget(title)
        close_btn.setIcon(QIcon(":/close.png"))
        close_btn.setIconSize(QSize(24, 24))
        header_layout.addWidget(close_btn)
        close_btn.clicked.connect(self.close_dialog)

        header.setLayout(header_layout)
        header.setProperty("class", "header")
        content.setProperty("class", "content")
        self.setStyleSheet("""
            Dialog {
                background-color: rgba(0, 0, 0, .2);
            }
        
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
            
            .content {
                background-color: #fff;
            }
            
       """)

    def close_dialog(self):
        self.done(0)
