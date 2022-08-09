from PySide6.QtWidgets import QWidget

from .Panel import Panel
from .DownloadingItem import DownloadingItem
from ..enums import EventName


class DownloadingPanel(Panel):
    def __init__(self, parent: QWidget = None):
        super().__init__(
            parent=parent,
            widget=QWidget()
        )
        self.set_current_index(0)

    def add_item(
        self,
        *,
        name: str,
        aid: int,
        cid: int,
        vid: str,
        album: str,
        quality: int
    ):
        if self.get_current_index() == 0:
            self.set_current_index(1)

        layout = self._widget.layout()
        layout.addWidget(
            DownloadingItem(
                self,
                name=name,
                album=album,
                aid=aid,
                cid=cid,
                vid=vid,
                quality=quality
            )
        )
