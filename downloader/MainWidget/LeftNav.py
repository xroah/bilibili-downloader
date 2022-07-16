from PySide6 import QtWidgets


class LeftNav(QtWidgets.QWidget):
    def __init__(self, parent: QtWidgets.QWidget = None):
        super().__init__(parent)
        layout = QtWidgets.QVBoxLayout(parent)
        self.downloading_btn = QtWidgets.QPushButton(parent=self, text="正在下载")
        self.downloaded_btn = QtWidgets.QPushButton(parent=self, text="已下载")
        layout.addWidget(self.downloading_btn)
        layout.addWidget(self.downloaded_btn)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addStretch()
        self.setStyleSheet(
            """
            background-color: red;
            """
        )
        self.setLayout(layout)
