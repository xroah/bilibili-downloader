from PySide6.QtWidgets import QWidget

from .Panel import Panel
from .DownloadingItem import DownloadingItem


class DownloadingPanel(Panel):
    def __init__(self, parent: QWidget = None):
        super().__init__(
            parent=parent,
            widget=QWidget()
        )
        self.set_current_index(1)
