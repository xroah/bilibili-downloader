from PySide6 import QtWidgets
from PySide6.QtCore import Qt


class LeftNav(QtWidgets.QWidget):
    def __init__(self, parent: QtWidgets.QWidget = None):
        super().__init__(parent)
        layout = QtWidgets.QVBoxLayout(parent)
        self.downloading_btn = QtWidgets.QPushButton(parent=self, text="正在下载")
        self.downloaded_btn = QtWidgets.QPushButton(parent=self, text="已下载")
        self.downloading_btn.setProperty("class", "downloading-btn")
        self.downloading_btn.setCursor(Qt.PointingHandCursor)
        self.downloaded_btn.setCursor(Qt.PointingHandCursor)
        layout.addWidget(self.downloading_btn)
        layout.addWidget(self.downloaded_btn)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addStretch()
        layout.setSpacing(0)
        self.setAttribute(Qt.WA_StyledBackground)
        self.setLayout(layout)
        self.set_qss()
        self.downloading_btn.clicked.connect(self.downloading_btn_click)
        self.downloaded_btn.clicked.connect(self.downloaded_btn_click)

    def downloading_btn_click(self):
        print("downloading btn")

    def downloaded_btn_click(self):
        print("downloaded btn")

    def set_qss(self):
        self.setStyleSheet("""
            LeftNav {
                background-color: #fff;
                border-right: 1px solid rgba(0, 0, 0, .2);
            }

            QPushButton {
                padding: 10px;
                border: none;
            }

            QPushButton:hover {
                background-color: rgba(13, 110, 253, .5);
                color: #fff;
            }

            QPushButton.active {
                background-color: red;
            }

            QPushButton.downloading-btn {
                border-bottom: 1px solid #f0f0f0;
            }
        """)
