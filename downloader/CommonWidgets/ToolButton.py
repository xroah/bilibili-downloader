from PySide6.QtWidgets import QToolButton, QWidget
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon


class ToolButton(QToolButton):
    def __init__(self, parent: QWidget = None, icon: str = ""):
        super().__init__(parent)
        self.setCursor(Qt.PointingHandCursor)

        if icon:
            self.setIcon(QIcon(icon))
