from PySide6.QtWidgets import QWidget

from ..utils import utils
from ..common_widgets import CheckableItem
from .ProgressBar import ProgressBar


class DownloadingItem(CheckableItem):
    def __init__(self, parent: QWidget = None):
        super().__init__(widget=ProgressBar(), parent=parent)
        self.paused = True
        self._progress_bar = self._widget
        self._ctx_menu.addAction("开始/暂停")
        self._ctx_menu.addAction("打开文件夹")
        self._ctx_menu.addAction("删除")
        self._ctx_menu.addAction("属性")
        self.setProperty("class", "downloading-item")
        self.setStyleSheet(utils.get_style("downloading-item"))

