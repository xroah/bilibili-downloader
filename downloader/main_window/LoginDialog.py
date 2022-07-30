from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import (
    QDialog,
    QMainWindow,
    QVBoxLayout,
    QHBoxLayout,
    QStackedWidget,
    QProgressBar
)
from PySide6.QtCore import Qt, QUrl, Signal
from PySide6.QtNetwork import QNetworkCookie

from ..common_widgets import PushButton, MessageBox
from ..enums import Req
from ..cookie import Cookie

import sys
from typing import cast


class LoginDialog(QDialog):
    login_success = Signal()

    def __init__(self, parent=QMainWindow):
        super().__init__(parent)
        self.stacked = QStackedWidget(self)
        self.progress_bar = QProgressBar(self)
        self.cookies = dict()
        self.cookie = Cookie()
        layout = QVBoxLayout()
        view = QWebEngineView(self)
        self.view = view
        self.page = view.page()
        cookie_store = self.page.profile().cookieStore()
        view.load(cast(str, Req.LOGIN_PAGE.value))
        layout.addWidget(self.stacked, 1)
        layout.setContentsMargins(0, 0, 0, 0)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setValue(0)
        self.page.loadProgress.connect(self.progress_update)
        self.page.loadFinished.connect(self.load_finished)
        self.page.urlChanged.connect(self.url_changed)
        cookie_store.cookieAdded.connect(self.cookie_added)
        cookie_store.cookieRemoved.connect(self.cookie_removed)
        self.stacked.addWidget(view)
        self.stacked.addWidget(self.progress_bar)
        self.stacked.setCurrentIndex(1)

        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setFixedSize(450, 500)
        self.setContextMenuPolicy(Qt.NoContextMenu)
        self.setWindowTitle("登录")
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        self.setLayout(layout)

        # The modal dialog has no close button on macos
        if sys.platform == "darwin":
            footer_layout = QHBoxLayout()
            close_btn = PushButton(self, "关闭")
            footer_layout.setAlignment(Qt.AlignCenter)
            footer_layout.addWidget(close_btn)
            footer_layout.setContentsMargins(0, 0, 0, 0)
            close_btn.clicked.connect(lambda: self.reject())
            layout.addLayout(footer_layout)

        self.open()

    def cookie_added(self, cookie: QNetworkCookie):
        name = cookie.name().toStdString()
        value = cookie.name().toStdString()
        self.cookies[name] = value

    def cookie_removed(self, cookie: QNetworkCookie):
        name = cookie.name().toStdString()
        if name in self.cookies:
            del self.cookies[name]

    def url_changed(self, url: QUrl):
        print("changed", url.url())
        if "redirect" in url.url():
            cookie_text = []
            for k, v in self.cookies.items():
                cookie_text.append(f"{k}={v}")
            cookie_text = "; ".join(cookie_text)
            self.cookie.set(cookie_text)
            self.accept()
            self.login_success.emit()

    def progress_update(self, progress: int):
        self.progress_bar.setValue(progress)

    def load_finished(self, ok):
        self.stacked.setCurrentIndex(0)
        if not ok:
            MessageBox.alert("加载失败")
        else:
            self.update_style()

    def update_style(self):
        self.view.page().runJavaScript(
            """
                (function() {
                    let style = document.createElement("style")
                    style.innerHTML = `
                        #tab-nav .t {
                            opacity: 0;
                        }
                        
                        #tab-nav .register,
                        #keep-me-in,
                        .login-explain,
                        .qr-text {
                           display: none; 
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
