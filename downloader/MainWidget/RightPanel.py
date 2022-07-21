from PySide6.QtWidgets import (
    QStackedWidget,
    QVBoxLayout,
    QWidget,
    QLabel,
    QScrollArea
)


class RightPanel(QWidget):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self.stacked = QStackedWidget(self)
        text1 = QLabel(parent=self, text="正在下载")
        text2 = QLabel(parent=self, text="已下载")
        self.stacked.addWidget(text1)
        self.stacked.addWidget(text2)
        layout = QVBoxLayout(self)
        layout.addWidget(self.stacked)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

    def set_current_index(self, i: int):
        self.stacked.setCurrentIndex(i)
