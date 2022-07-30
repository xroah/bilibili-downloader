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
            on_ok: Callable[[int, list], None] = None
    ):
        super().__init__(
            parent=cast(QMainWindow, parent),
            size=QSize(260, 150),
            ok_callback=self.on_ok
        )
        select = QComboBox(self)
        self.data = data
        self.select = select
        self.on_ok = on_ok
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

    def on_ok(self):
        if self.on_ok:
            self.on_ok(self.select.currentData())
