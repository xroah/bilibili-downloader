from typing import cast

from PySide6.QtWidgets import (
    QProgressBar,
    QVBoxLayout,
    QWidget,
    QToolButton
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon
from PySide6.QtUiTools import QUiLoader

from ..utils import utils


class DownloadingItem(QProgressBar):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self.paused = True
        self.init_layout()

    def init_layout(self):
        layout = QVBoxLayout()
        loader = QUiLoader()
        widget = loader.load(utils.get_resource_path("uis/downloading-item.ui"))
        icon = cast(
            QToolButton,
            widget.findChild(QToolButton, "icon")
        )
        toggle_btn = cast(
            QToolButton,
            widget.findChild(QToolButton, "toggle")
        )
        icon.setIcon(utils.get_icon("video"))
        icon.setIconSize(QSize(50, 50))
        toggle_btn.setIcon(QIcon(utils.get_icon("play")))
        toggle_btn.setIconSize(QSize(32, 32))
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(widget)
        self.setTextVisible(False)
        self.setValue(50)
        self.setLayout(layout)
        self.setProperty("class", "downloading-item")
        self.setStyleSheet(utils.get_style("downloading-item"))

