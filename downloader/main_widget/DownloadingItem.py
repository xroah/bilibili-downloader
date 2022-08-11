from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QToolButton,
    QProgressBar,
)
from PySide6.QtGui import QContextMenuEvent
from PySide6.QtCore import Signal, QObject, QSize
from PySide6.QtUiTools import QUiLoader

from ..utils import utils
from ..enums import Status
from ..common_widgets import CheckableItem


class DownloadingItem(CheckableItem):
    status_changed = Signal(QObject, Status)

    def __init__(
            self,
            parent: QWidget = None,
            *,
            name: str,
            cid: int,
            aid: int,
            vid: str,
            album: str,
            quality: int
    ):
        loader = QUiLoader()
        widget = loader.load(utils.get_resource_path("uis/downloading-item.ui"))
        super().__init__(widget=widget, parent=parent)
        self.paused = False
        self.downloaded_size = 0
        self.total = 0
        self.video_name = utils.get_child(widget, QLabel, "videoName")
        self.toggle_btn = utils.get_child(widget, QToolButton, "toggle")
        self.hint_label = utils.get_child(widget, QLabel, "hint")
        self.downloaded_label = utils.get_child(widget, QLabel, "downloaded")
        self.total_label = utils.get_child(widget, QLabel, "total")
        self._progress = utils.get_child(widget, QProgressBar, "progressBar")
        self.toggle_btn.setStyleSheet(utils.get_style("toolbutton"))
        self.toggle_btn.setIconSize(QSize(32, 32))
        self._ctx_menu.addAction("开始/暂停")
        self._ctx_menu.addAction("打开文件夹")
        self._ctx_menu.addAction("删除")
        self.setProperty("vid", vid)
        self.setProperty("cid", cid)
        self.setProperty("aid", aid)
        self.setProperty("name", name)
        self.setProperty("album", album)
        self.setProperty("quality", quality)
        self.video_name.setText(name)
        self.setStyleSheet(utils.get_style("downloading-item"))
        self.start()

        self.toggle_btn.clicked.connect(self.toggle)

    def update_downloaded(self, size: float):
        self.downloaded_size += size
        self.downloaded_label.setText(
            utils.format_size(self.downloaded_size)
        )
        self.update_progress()

    def update_speed(self, speed: float):
        self.set_hint_text(utils.format_size(speed) + "/s")

    def update_total(self, total: float):
        self.total = total
        self.total_label.setText(utils.format_size(total))

    def update_progress(self):
        if self.total > 0:
            p = (self.downloaded_size / self.total) * 100
            v = self._progress.value()

            if v != p:
                self._progress.setValue(int(p))

    def emit_change(self, status: Status):
        self.status_changed.emit(self, status)

    def _pause(self):
        self.pause()
        self.emit_change(Status.PAUSE)

    def pause(self):
        self.paused = True
        self.toggle_btn.setIcon(utils.get_icon("play"))
        self.set_hint_text("已暂停")

    def _start(self):
        self.start()
        self.emit_change(Status.START)

    def start(self):
        self.paused = False
        self.toggle_btn.setIcon(utils.get_icon("pause"))
        self.set_hint_text("等待开始")

    def toggle(self):
        if self.paused:
            self._start()
        else:
            self._pause()

    def set_hint_text(self, text: str, error=False):
        if error:
            self.pause()

        self.hint_label.setText(text)
        self.hint_label.setStyleSheet("color: red;" if error else "")

    def contextMenuEvent(self, e: QContextMenuEvent):
        pos = e.pos()
        g = self.toggle_btn.geometry()

        # mouse pointer within toggle button
        if (
                g.x() <= pos.x() <= g.width() + g.x() and
                g.y() <= pos.y() <= g.y() + g.height()
        ):
            return

        super().contextMenuEvent(e)
