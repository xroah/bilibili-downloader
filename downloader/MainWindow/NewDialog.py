import json
from urllib.parse import urlencode
from threading import Thread

from ..CommonWidgets import Dialog
from ..utils import utils
from ..CommonWidgets import Input, MessageBox
from .Loading import Loading
from ..Enums import Req
from .SelectDialog import SelectDialog

import httpx
from PySide6.QtCore import QSize, Signal
from PySide6.QtWidgets import (
    QLabel,
    QWidget,
    QVBoxLayout
)


class NewDialog(Dialog):
    hide_loading = Signal()
    req_error = Signal(str)
    # pages, resolution, dict
    req_success = Signal(list, dict)

    def __init__(self, window):
        super().__init__(
            parent=window,
            title="新建下载",
            show_cancel=True,
            size=QSize(420, 150),
            is_modal=True,
            close_on_ok=False,
            ok_callback=self.on_ok
        )
        self._window = window
        self.loading: Loading | None = None
        self._input = Input()
        self.pages = []
        self.bv = ""

        self.req_error.connect(self.handle_error)
        self.hide_loading.connect(self.handle_loading)
        self.req_success.connect(self.handle_success)
        self.shown.connect(lambda: self._input.setFocus())
        self.init()
        self.open_()

    def init(self):
        content = QWidget()
        layout = QVBoxLayout()
        input_ = self._input
        input_.setParent(content)
        input_.setFrame(False)
        input_.setProperty("class", "input")

        layout.addWidget(QLabel("输入BV号/视频地址"))
        layout.addWidget(input_)
        layout.setContentsMargins(5, 5, 5, 5)

        content.setProperty("class", "new-dialog")
        content.setLayout(layout)
        content.setStyleSheet(utils.get_style("new-dialog"))
        self.set_content(content)

    def show_msg(self, t: str):
        MessageBox.alert(t, parent=self)
        
    def handle_error(self, msg: str):
        self.handle_loading()
        self.show_msg(msg)

    def handle_loading(self):
        if self.loading is None:
            return

        self.loading.accept()
        self.loading = None

    def request(self, path, params) -> dict | None:
        headers = {
            "referer": Req.REFERER.value,
            "user-agent": Req.USER_AGENT.value
        }

        try:
            res = httpx.get(
                f"{Req.API_ADDR}{path}?{params}",
                headers=headers
            )
            j = json.loads(res.text)
        except Exception as e:
            print("Request error:", e)
            self.req_error.emit(str(e))
            return None
        else:
            if j["code"] != 0:
                self.req_error.emit(
                    j["message"] if "message" in j else "请求错误"
                )
                return None

            return j["data"]

    def fet_video_info(self, bv: str):
        d = self.request(Req.LIST_PATH, f"bvid={bv}&jsonp=jsonp")
        if not d:
            self.hide_loading.emit()
            return
        query = {
            "cid": d[0]["cid"],
            "bvid": bv,
            "otype": "json"
        }
        pages = d
        d = self.request(Req.URL_PATH, urlencode(query))
        self.hide_loading.emit()
        
        if d:
            keys = d["accept_description"]
            values = d["accept_quality"]
            self.req_success.emit(pages, dict(zip(keys, values)))

    def handle_success(self, pages: list, d: dict[str, int]):
        self.pages = pages
        SelectDialog(
            parent=self,
            data=d,
            on_ok=self.on_select_resolution
        )

    def on_select_resolution(self, sel: int, all_: list):
        self.accept()
        self._window.download.emit(self.bv, sel, all_, self.pages)

    def on_ok(self):
        text = self._input.text().strip()
        bv = utils.parse_url(text)

        if not text:
            self.show_msg("内容不能为空")
            return

        if not bv:
            self.show_msg("没有找到视频")
            return

        self.loading = Loading(self)
        self.bv = bv

        t = Thread(target=self.fet_video_info, args=(bv, ))
        t.start()
