from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import (
    QDialog,
    QMainWindow,
    QVBoxLayout
)
from PySide6.QtCore import Qt


class LoginDialog(QDialog):
    def __init__(self, parent=QMainWindow):
        super().__init__(parent)
        layout = QVBoxLayout()
        view = QWebEngineView(self)
        self.view = view
        view.load("https://passport.bilibili.com/ajax/miniLogin/minilogin")
        view.page().titleChanged.connect(self.title_changed)
        layout.addWidget(view)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)
        self.setFixedSize(450, 500)
        self.setWindowTitle("登录")
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        self.open()

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
