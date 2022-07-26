import json
import re
from urllib.parse import urlparse

from ..CommonWidgets import Dialog
from ..utils import utils
from ..CommonWidgets import Input, MessageBox
from .Loading import Loading

import httpx
from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import (
    QLabel,
    QMainWindow,
    QWidget,
    QVBoxLayout
)


class NewDialog:
    def __init__(self, window: QMainWindow):
        self.dialog = Dialog(
            title="新建下载",
            parent=window,
            show_cancel=True,
            size=QSize(420, 150),
            close_on_ok=False,
            ok_callback=self.on_ok
        )
        self._input = Input()
        self.init()
        self.dialog.open_()

    def init(self):
        content = QWidget()
        layout = QVBoxLayout()
        input_ = self._input
        input_.setParent(content)
        input_.setFrame(False)
        input_.setProperty("class", "input")

        layout.addWidget(QLabel("输入BV号/视频地址"))
        layout.addWidget(input_)
        content.setProperty("class", "new-dialog")
        content.setLayout(layout)
        content.setStyleSheet(utils.get_style("new-dialog"))
        layout.setContentsMargins(5, 5, 5, 5)

        self.dialog.shown.connect(lambda: input_.setFocus())
        self.dialog.set_content(content)

    def show_msg(self, t: str):
        MessageBox.alert(t, parent=self.dialog)

    def on_ok(self):
        text = self._input.text().strip()
        bv = utils.parse_url(text)

        if not text:
            self.show_msg("内容不能为空")
            return

        if not bv:
            self.show_msg("没有找到视频")
            return

        # loading = Loading(self.dialog)
        headers = {
            "referer": "https://www.bilibili.com",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
        }
        res = httpx.get(
            f"https://api.bilibili.com/x/player/pagelist?bvid={bv}&jsonp=jsonp",
            headers=headers
        )

        try:
            j = json.loads(res.text)
        except Exception as e:
            print("====>", e)
            self.show_msg("未知错误")
            return

        if j["code"] != 0:
            self.show_msg(j["message"] if "message" in j else "请求错误")

        print(j)