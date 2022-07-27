from ..CommonWidgets import Dialog

from PySide6.QtWidgets import (
    QComboBox,
    QWidget,
    QLabel,
    QVBoxLayout
)
from PySide6.QtCore import QSize


class SelectDialog(Dialog):
    def __init__(self, parent: QWidget, data: dict[str, int]):
        super().__init__(
            parent=parent,
            size=QSize(260, 150),
            is_modal=True,
            ok_callback=self.on_ok
        )
        select = QComboBox(self)
        self.select = select
        content = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("选择分辨率"))
        layout.addWidget(select)

        for k, v in data.items():
            select.addItem(k, v)

        content.setLayout(layout)
        self.set_content(content)
        self.open_()

    def on_ok(self):
        print(self.select.currentData())
