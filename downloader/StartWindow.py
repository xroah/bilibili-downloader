from PySide6.QtWidgets import (
    QMainWindow,
    QLabel,
    QProgressBar,
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
        progress = QProgressBar(widget)
        label.setScaledContents(True)
        label.setPixmap(QPixmap(utils.get_resource_path("start.png")))
        progress.setMaximum(0)
        progress.setMinimum(0)
        progress.setStyleSheet("""
            QProgressBar:chunk {
                max-height: 8px;
                height: 8px;
                background-color: #00aeec;
            }
        """)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(label)
        layout.addWidget(progress)
        widget.setLayout(layout)

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setFixedSize(360, 190)
        self.setCentralWidget(widget)
        self.show()
