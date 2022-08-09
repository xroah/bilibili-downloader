from PySide6.QtWidgets import QWidget

from .Panel import Panel
from .DownloadingItem import DownloadingItem
from ..utils import event_bus
from ..enums import EventName


class DownloadingPanel(Panel):
    def __init__(self, parent: QWidget = None):
        super().__init__(
            parent=parent,
            widget=QWidget()
        )
        self.set_current_index(0)
        event_bus.on(EventName.NEW_DOWNLOAD, self.new_download)

    def add_item(
        self,
        *,
        name: str,
        aid: int,
        cid: int,
        vid: str
    ):
        if self.get_current_index() == 0:
            self.set_current_index(1)

    def new_download(self, data):
        pass