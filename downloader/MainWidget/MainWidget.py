from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QPushButton
)
from .LeftNav import LeftNav
from .RightPanel import RightPanel


class MainWidget(QWidget):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        left_nav = LeftNav(self)
        right = RightPanel(self)
        self.left_nav = left_nav
        self.right_panel = right
        right.setStyleSheet("background-color: #fff;")

        layout = QHBoxLayout()
        layout.addWidget(left_nav, 1)
        layout.addWidget(right, 5)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        left_nav.changed.connect(self.handle_tab_change)

    def handle_tab_change(self, btn: QPushButton):
        classname = btn.property("class")
        d: dict[str, int] = {
            "downloading-btn": 0,
            "downloaded-btn": 1
        }
        self.right_panel.set_current_index(d[classname])
        print("change", btn.property("class"))
