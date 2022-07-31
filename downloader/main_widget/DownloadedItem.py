from typing import cast

from PySide6.QtWidgets import QWidget, QLabel
from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QIcon
from PySide6.QtUiTools import QUiLoader

from ..utils import utils
from ..common_widgets import CheckableItem


class DownloadedItem(CheckableItem):
    def __init__(self, parent: QWidget = None, deleted: bool = False):
        loader = QUiLoader()
        widget = loader.load(utils.get_resource_path("uis/downloaded-item.ui"))
        super().__init__(
            parent=parent,
            widget=widget
        )

        if not deleted:
            label = cast(
                QLabel,
                widget.findChild(QLabel, "deletedText")
            )
            layout = widget.layout()
            if label and layout:
                layout.removeWidget(label)
                label.deleteLater()

        self.setProperty(
            "class",
            f"downloaded-item{'-deleted' if deleted else ''}"
        )
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet(utils.get_style("downloaded-item"))
