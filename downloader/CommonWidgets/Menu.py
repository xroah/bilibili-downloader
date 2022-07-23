from PySide6.QtWidgets import (
    QMenu, 
    QWidget
)
from PySide6.QtCore import Qt

from ..utils import utils


class Menu(QMenu):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self.setWindowFlag(Qt.FramelessWindowHint, True)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setStyleSheet(utils.get_style("menu"))
