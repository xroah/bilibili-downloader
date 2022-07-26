from PySide6.QtWidgets import QPushButton, QWidget
from PySide6.QtCore import Qt

from ..utils import utils


class PushButton(QPushButton):
    def __init__(
            self,
            parent: QWidget = None,
            text: str = "",
            primary: bool = True,
            classname: str = ""
    ):
        super().__init__(parent=parent, text=text)
        self.setCursor(Qt.PointingHandCursor)
        self.setFocusPolicy(Qt.StrongFocus)

        if classname:
            self.setProperty("class", classname)

        if primary:
            self.setProperty("class", "primary")

        ss = utils.get_style("pushbutton")
        self.setStyleSheet(ss)
