from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QHBoxLayout,
    QPushButton
)
from .LeftNav import LeftNav


class MainWidget(QWidget):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        left_nav = LeftNav(self)
        right = QLabel(self)
        right.setText("列表。。。")
        right.setStyleSheet("background-color: #fff;")

        layout = QHBoxLayout()
        layout.addWidget(left_nav, 1)
        layout.addWidget(right, 5)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        left_nav.changed.connect(self.handle_tab_change)

    def handle_tab_change(self, btn: QPushButton):
        print("change", btn.property("class"))
