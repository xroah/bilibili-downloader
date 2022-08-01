from typing import Callable, cast

from PySide6.QtWidgets import (
    QComboBox,
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QMainWindow
)
from PySide6.QtCore import QSize, Qt

from ..common_widgets import Dialog


class SelectDialog(Dialog):
    def __init__(
            self,
            *,
            parent: QWidget,
            data: dict[str, int],
            ok_callback: Callable[[int], None],
            title: str
    ):
        super().__init__(
            parent=cast(QMainWindow, parent),
            size=QSize(360, 180),
            show_cancel=True,
            ok_callback=ok_callback
        )
        select = QComboBox(self)
        self.data = data
        self.select = select
        content = QWidget()
        layout = QVBoxLayout()
        title_layout = QHBoxLayout()
        resolution_layout = QHBoxLayout()
        title_label = QLabel(title)
        title_label.setWordWrap(True)
        title_layout.addWidget(QLabel("<strong>标 题:</strong> "))
        title_layout.addWidget(title_label, 1)
        title_layout.setAlignment(Qt.AlignTop)
        resolution_layout.addWidget(QLabel("<strong>分辨率:</strong> "))
        resolution_layout.addWidget(select, 1)
        layout.addStretch()
        layout.addLayout(title_layout)
        layout.addLayout(resolution_layout)
        layout.addStretch()
        layout.setSpacing(8)
        select.setStyleSheet("""
            padding: 5px;
            min-height: 20px;
        """)

        for k, v in data.items():
            select.addItem(k, v)

        content.setLayout(layout)
        self.setWindowTitle("选择分辨率")
        self.set_content(content)
        self.open()

    def ok(self):
        self.accept()
        if self.ok_callback:
            self.ok_callback(self.select.currentData())
