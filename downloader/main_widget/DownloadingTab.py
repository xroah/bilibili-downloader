from PySide6.QtWidgets import QWidget

from .Tab import Tab
from .DownloadingItem import DownloadingItem


class DownloadingTab(Tab):

    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self.set_current_index(0)

    def add_item(self, item: DownloadingItem):
        if self.get_current_index() == 0:
            self.set_current_index(1)

        layout = self._widget.layout()
        item.set_parent(self)
        layout.addWidget(item)
