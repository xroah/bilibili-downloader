from PySide6.QtWidgets import QWidget, QVBoxLayout

from .Panel import Panel
from .DownloadingItem import DownloadingItem


class DownloadingPanel(Panel):
    def __init__(self, parent: QWidget = None):
        super().__init__(
            parent=parent,
            widget=QWidget()
        )
        widget = self._widget
        layout = widget.layout()
        layout.addWidget(DownloadingItem(self))
        layout.addWidget(DownloadingItem(self))
        layout.addWidget(DownloadingItem(self))
        layout.addWidget(DownloadingItem(self))
        layout.addWidget(DownloadingItem(self))
        layout.addWidget(DownloadingItem(self))
        layout.addWidget(DownloadingItem(self))
        layout.addWidget(DownloadingItem(self))
        layout.addWidget(DownloadingItem(self))
        layout.addWidget(DownloadingItem(self))
        widget.setLayout(layout)
        self._layout.setCurrentIndex(1)
