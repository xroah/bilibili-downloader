from typing import Callable, cast

from PySide6.QtWidgets import (
    QComboBox,
    QWidget,
    QLabel,
    QVBoxLayout,
    QMainWindow
)
from PySide6.QtCore import QSize

from ..common_widgets import Dialog


class SelectDialog(Dialog):
    def __init__(
            self,
            *,
            parent: QWidget,
            data: dict[str, int],
            ok_callback: Callable[[int], None]
    ):
        super().__init__(
            parent=cast(QMainWindow, parent),
            size=QSize(260, 150),
            ok_callback=ok_callback
        )
        select = QComboBox(self)
        self.data = data
        self.select = select
        content = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("选择分辨率"))
        layout.addWidget(select)
        select.setStyleSheet("""
            padding: 5px;
            min-height: 20px;
        """)

        for k, v in data.items():
            select.addItem(k, v)

        content.setLayout(layout)
        self.set_content(content)
        self.open()

    def ok(self):
        self.accept()
        if self.ok_callback:
            self.ok_callback(self.select.currentData())
