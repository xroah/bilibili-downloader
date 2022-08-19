from PySide6.QtCore import Signal, QObject
from PySide6.QtWidgets import QWidget

from .Tab import Tab
from .DownloadedItem import DownloadedItem


class DownloadedTab(Tab):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self.set_current_index(0)

    def insert_item(self, item: DownloadedItem):
        if self.get_current_index() == 0:
            self.set_current_index(1)

        layout = self._widget.layout()
        item.set_parent(self)
        layout.insertWidget(0, item)
