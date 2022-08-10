from PySide6.QtWidgets import (
    QMainWindow,
    QLabel,
    QWidget,
    QVBoxLayout
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap

from .utils import utils


class StartWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        widget = QWidget(self)
        layout = QVBoxLayout()
        label = QLabel(parent=widget)
        label.setScaledContents(True)
        label.setPixmap(QPixmap(utils.get_resource_path("start.png")))
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(label)
        widget.setLayout(layout)

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setFixedSize(360, 180)
        self.setCentralWidget(widget)
        self.show()
