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
        self.set_current_index(1)
        event_bus.on(EventName.NEW_DOWNLOAD, self.new_download)

    def new_download(self, data):
        print(data)