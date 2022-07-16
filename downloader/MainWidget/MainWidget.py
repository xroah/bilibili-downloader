import PySide6.QtWidgets as QtWidgets
from .LeftNav import LeftNav


class MainWidget(QtWidgets.QWidget):
    def __init__(self, parent: QtWidgets.QWidget = None):
        super().__init__(parent)
        left_nav = LeftNav(self)
        right = QtWidgets.QLabel(self)
        right.setText("列表。。。")
        right.setStyleSheet("background-color: #fff;")
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(left_nav, 1)
        layout.addWidget(right, 5)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(layout)

    def handle_click(self):
        print("click")
        self.button.setStyleSheet("")
