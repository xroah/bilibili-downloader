from threading import Thread
import traceback

from PySide6.QtCore import QSize, Signal
from PySide6.QtGui import QShowEvent, QClipboard
from PySide6.QtWidgets import (
    QLabel,
    QWidget,
    QVBoxLayout,
    QMainWindow
)

from ..common_widgets import Dialog
from ..utils import utils, request, event_bus
from ..common_widgets import Input, MessageBox
from .Loading import Loading
from ..enums import Req, EventName
from .SelectDialog import SelectDialog
from ..utils.parse_video_page import parse
from ..db import DB


class NewDialog(Dialog):
    hide_loading = Signal()
    req_error = Signal(str)
    req_success = Signal(dict)

    def __init__(self, window: QMainWindow):
        super().__init__(
            parent=window,
            title="新建下载",
            show_cancel=True,
            size=QSize(420, 150)
        )
        self.data = dict()
        self._window = window
        self.loading: Loading | None = None
        self._input = Input()

        self.req_error.connect(self.handle_error)
        self.hide_loading.connect(self.close)
        self.req_success.connect(self.handle_success)
        self.init()
        self.open()

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
        self.close_loading()
        self.show_msg(msg)

    def close_loading(self):
        if self.loading is None:
            return

        self.loading.close()
        self.loading = None

    def handle_success(self, d: dict[str, any]):
        self.data = d
        self.close_loading()
        self.show_select_dialog(d["title"])

    def show_select_dialog(self, title: str):
        SelectDialog(
            parent=self,
            data=self.data["qualities"],
            ok_callback=self.on_select_resolution,
            title=title
        )

    def on_select_resolution(self, sel: int):
        self.accept()
        self.data["quality"] = sel
        with DB() as db:
            db.insert(self.data)
        event_bus.emit(EventName.NEW_DOWNLOAD, self.data)

    def fet_video_info(self, bv: str):
        try:
            res = request.get(f"{Req.VIDEO_PAGE.value}{bv}", timeout=30)
        except Exception as e:
            self.req_error.emit(str(e))
        else:
            try:
                ret = parse(res.text)
            except Exception:
                traceback.print_exc()
                self.req_error.emit("解析错误")
            else:
                if not ret["bvid"]:
                    self.req_error.emit("视频不存在")
                    return

                self.req_success.emit(ret)

    def ok(self):
        text = self._input.text().strip()
        bv = utils.parse_url(text)

        if not text:
            self.show_msg("内容不能为空")
            return
        if not bv:
            self.show_msg("视频ID错误")
            return
        if "bvid" in self.data and self.data["bvid"] == bv:
            self.show_select_dialog(self.data["title"])
            return

        self.loading = Loading(self)
        t = Thread(target=self.fet_video_info, args=(bv,))
        t.daemon = True
        t.start()

    def showEvent(self, e: QShowEvent) -> None:
        clipboard = QClipboard()
        text = clipboard.text(QClipboard.Clipboard)

        if text:
            bv = utils.parse_url(text)

            if bv:
                self._input.setText(bv)

        self._input.setFocus()
