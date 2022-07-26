from PySide6.QtWidgets import (
    QDialog,
    QProgressBar,
    QWidget,
    QHBoxLayout
)
from PySide6.QtCore import Qt


class Loading(QDialog):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        pb = QProgressBar(self)
        layout = QHBoxLayout()
        layout.addWidget(pb)
        layout.setContentsMargins(5, 5, 5, 5)
        pb.setMinimum(0)
        pb.setMaximum(0)
        pb.setTextVisible(False)

        self.setModal(True)
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        self.setFixedSize(160, 50)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setLayout(layout)
        self.open()
