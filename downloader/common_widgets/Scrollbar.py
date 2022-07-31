from PySide6.QtWidgets import QScrollBar, QWidget
from PySide6.QtGui import QPalette

from ..utils import utils


class Scrollbar(QScrollBar):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        palette = self.palette()
        palette.setColor(QPalette.Window, "transparent")
        self.setPalette(palette)
        self.setStyleSheet(utils.get_style("scrollbar"))
