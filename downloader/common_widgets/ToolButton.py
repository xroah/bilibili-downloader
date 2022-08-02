from PySide6.QtWidgets import QToolButton, QWidget
from PySide6.QtCore import Qt, QSize

from ..utils import utils


class ToolButton(QToolButton):
    def __init__(
            self,
            parent: QWidget = None,
            icon: str = "",
            icon_size: int = 36
    ):
        super().__init__(parent)
        self.setCursor(Qt.PointingHandCursor)
        self.setStyleSheet(utils.get_style("toolbutton"))

        if icon:
            self.setIcon(utils.get_icon(icon))
            self.setIconSize(QSize(icon_size, icon_size))
