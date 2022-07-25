from inspect import stack
from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QPushButton,
    QStackedWidget
)

from .LeftNav import LeftNav
from .Panel import Panel
from ..utils import utils


class MainWidget(QWidget):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        left_nav = LeftNav(self)
        self.left_nav = left_nav
        self.right_panel = self.gen_right_panel()

        layout = QHBoxLayout()
        layout.addWidget(left_nav)
        layout.addWidget(self.right_panel, 1)
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
        self.set_current(d[classname])
        print("change", btn.property("class"))
        
    def gen_right_panel(self) -> QStackedWidget:
        stacked = QStackedWidget(self)
        qss = utils.get_style("main-widget")
        stacked.setProperty("class", "right-panel")
        stacked.setStyleSheet(qss)
        stacked.addWidget(Panel(self))
        stacked.addWidget(Panel(self))

        return stacked

    def set_current(self, i: int):
        self.right_panel.setCurrentIndex(i)
    
