from multiprocessing import parent_process
from typing import cast

from PySide6.QtWidgets import (
    QWidget, 
    QLabel,
    QToolButton
)
from PySide6.QtGui import QContextMenuEvent

from ..utils import utils
from ..common_widgets import CheckableItem
from .ProgressBar import ProgressBar


class DownloadingItem(CheckableItem):
    def __init__(
            self, 
            parent: QWidget = None,
            *
            name: str,
            cid: int,
            aid: int,
            vid: str
        ):
        super().__init__(widget=ProgressBar(), parent=parent)
        self.video_name = cast(
            QLabel,
            self.findChild(QLabel, "videoName")    
        )
        self.paused = False
        self.toggle_btn = cast(
            QToolButton,
            self.findChild(QToolButton, "toggle")
        )
        self.toggle_btn.setStyleSheet(utils.get_style("toolbutton"))
        self._ctx_menu.addAction("开始/暂停")
        self._ctx_menu.addAction("打开文件夹")
        self._ctx_menu.addAction("删除")
        self.setProperty("vid", vid)
        self.setProperty("cid", cid)
        self.setProperty("aid", aid)
        self.setProperty("name", name)
        self.video_name.setText(name)
        self.setProperty("class", "downloading-item")
        self.setStyleSheet(utils.get_style("downloading-item"))

    def contextMenuEvent(self, e: QContextMenuEvent):
        pos = e.pos()
        g = self.toggle_btn.geometry()
        
        # mouse pointer within toggle button
        if (
            pos.x() >= g.x() and
            pos.x() <= g.width() + g.x() and
            pos.y() >= g.y() and
            pos.y() <= g.y() + g.height()
        ):
            return
        
        super().contextMenuEvent(e)
