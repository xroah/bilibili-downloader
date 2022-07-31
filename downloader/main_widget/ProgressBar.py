from typing import cast

from PySide6.QtWidgets import (
    QProgressBar,
    QWidget,
    QToolButton,
    QHBoxLayout
)
from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon
from PySide6.QtUiTools import QUiLoader

from ..utils import utils


class ProgressBar(QProgressBar):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        layout = QHBoxLayout()
        loader = QUiLoader()
        widget = loader.load(utils.get_resource_path("uis/downloading-item.ui"))
        toggle_btn = cast(
            QToolButton,
            widget.findChild(QToolButton, "toggle")
        )
        toggle_btn.setIcon(QIcon(utils.get_icon("play")))
        toggle_btn.setIconSize(QSize(32, 32))
        layout.addWidget(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setTextVisible(False)
        self.setValue(50)
        self.setProperty("class", "progress-bar")
        self.setLayout(layout)
