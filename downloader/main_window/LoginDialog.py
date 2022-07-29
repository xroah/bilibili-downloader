from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import (
    QDialog,
    QMainWindow,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton
)
from PySide6.QtCore import Qt

import sys


class LoginDialog(QDialog):
    def __init__(self, parent=QMainWindow):
        super().__init__(parent)
        layout = QVBoxLayout()
        view = QWebEngineView(self)
        self.view = view
        self.page = view.page()
        view.load("https://passport.bilibili.com/ajax/miniLogin/minilogin")
        layout.addWidget(view)
        layout.setContentsMargins(0, 0, 0, 0)
        self.page.windowCloseRequested.connect(self.close_window)
        self.setLayout(layout)
        self.setFixedSize(450, 500)
        self.setContextMenuPolicy(Qt.NoContextMenu)
        self.setWindowTitle("登录")
        self.setAttribute(Qt.WA_DeleteOnClose, True)

        # The modal dialog has no close button on macos
        if sys.platform == "darwin":
            footer_layout = QHBoxLayout()
            close_btn = QPush
            footer_layout.addStretch()
            footer_layout.addWidget()
            layout.addLayout(footer_layout)

        self.open()

    def close_window(self):
        self.close()
        print("1111")

    def title_changed(self, _: str):
        self.view.page().runJavaScript(
            """
                (function() {
                    let style = document.createElement("style")
                    style.innerHTML = `
                        #tab-nav .t {
                            opacity: 0;
                        }
                        #close {
                            display: none;
                        }
                        #wrapper {
                            display: flex;
                            justify-content: center;
                            align-items: center;
                            background-color: #f0f0f0;
                        }
                        #content {
                            position: static;
                            margin: 0;
                        }
                    `
                    document.head.appendChild(style)
                })()
            """
        )
