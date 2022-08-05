from PySide6.QtWidgets import QWidget

from .Panel import Panel
from .DownloadedItem import DownloadedItem


class DownloadedPanel(Panel):
    def __init__(self, parent: QWidget = None):
        super().__init__(
            parent=parent,
            widget=QWidget()
        )
        widget = self._widget
        layout = widget.layout()
        layout.addWidget(DownloadedItem(self))
        layout.addWidget(DownloadedItem(self, True))
        self.set_current_index(1)
        