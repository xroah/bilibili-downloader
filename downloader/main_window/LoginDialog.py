import sys
from typing import cast

from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import (
    QDialog,
    QMainWindow,
    QVBoxLayout,
    QHBoxLayout,
    QStackedWidget,
    QProgressBar,
    QWidget
)
from PySide6.QtCore import Qt, QUrl, Signal
from PySide6.QtNetwork import QNetworkCookie

from ..common_widgets import PushButton, MessageBox
from ..enums import Req
from ..Cookie import Cookie


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
        # for center the progress bar
        widget = QWidget(self)
        w_layout = QVBoxLayout()
        self.view = view
        self.page = view.page()
        view.load(cast(str, Req.LOGIN_PAGE.value))
        layout.addWidget(self.stacked, 1)
        layout.setContentsMargins(0, 0, 0, 0)
        w_layout.addWidget(self.progress_bar)
        widget.setLayout(w_layout)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setValue(0)
        self.stacked.addWidget(view)
        self.stacked.addWidget(widget)
        self.stacked.setCurrentIndex(1)

        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setFixedSize(450, 480)
        self.setWindowTitle("登录")
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        self.setLayout(layout)
        self.set_footer()
        self.setStyleSheet("""
            QProgressBar {
                max-height: 30px;
            }
        """)
        self.init_event()
        self.open()

    def init_event(self):
        cookie_store = self.page.profile().cookieStore()
        self.page.loadProgress.connect(self.progress_update)
        self.page.loadFinished.connect(self.load_finished)
        self.page.urlChanged.connect(self.url_changed)
        cookie_store.cookieAdded.connect(self.cookie_added)
        cookie_store.cookieRemoved.connect(self.cookie_removed)

    def set_footer(self):
        # The modal dialog has no close button on macos
        if sys.platform == "darwin":
            layout = self.layout()
            footer_layout = QHBoxLayout()
            close_btn = PushButton(self, "关闭")
            footer_layout.setAlignment(Qt.AlignCenter)
            footer_layout.addWidget(close_btn)
            footer_layout.setContentsMargins(0, 0, 0, 0)
            close_btn.clicked.connect(lambda: self.reject())
            layout.addLayout(footer_layout)

    def cookie_added(self, cookie: QNetworkCookie):
        name = cookie.name().toStdString()
        value = cookie.value().toStdString()
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
        print("Load finished")
        self.stacked.setCurrentIndex(0)
        if not ok:
            MessageBox.alert("加载失败", parent=self)
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
