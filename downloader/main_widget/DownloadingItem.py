from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QToolButton
)
from PySide6.QtGui import QContextMenuEvent
from PySide6.QtCore import Signal, QObject

from ..utils import utils
from ..enums import Status
from ..common_widgets import CheckableItem
from .ProgressBar import ProgressBar


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
        progress = ProgressBar()
        super().__init__(widget=progress, parent=parent)
        self.paused = False
        self.downloaded_size = 0
        self.total = 0
        self._progress = progress
        self.video_name = utils.get_child(self, QLabel, "videoName")
        self.toggle_btn = utils.get_child(self, QToolButton, "toggle")
        self.speed_label = utils.get_child(self, QLabel, "speed")
        self.downloaded_label = utils.get_child(self, QLabel, "downloaded")
        self.total_label = utils.get_child(self, QLabel, "total")
        self.toggle_btn.setStyleSheet(utils.get_style("toolbutton"))
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
        self.setProperty("class", "downloading-item")
        self.setStyleSheet(utils.get_style("downloading-item"))
        self.start()

        self.toggle_btn.clicked.connect(self.toggle)

    def update_downloaded(self, size: float):
        self.downloaded_size += size
        self.downloaded_label.setText(
            utils.format_size(self.downloaded_size)
        )

    def update_speed(self, speed: float):
        self.speed_label.setText(utils.format_size(speed) + "/s")

    def update_total(self, total: float):
        self.total_label.setText(utils.format_size(total))

    def update_progress(self):
        if self.total > 0:
            p = self.downloaded_size / self.total
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

    def set_hint_text(self, text: str):
        self.speed_label.setText(text)

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
