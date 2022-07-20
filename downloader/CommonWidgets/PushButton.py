from PySide6.QtWidgets import QPushButton, QWidget
from PySide6.QtCore import Qt

from ..Enums import Color
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

        if classname:
            self.setProperty("class", classname)

        if primary:
            self.setProperty("class", "primary")

        ss_filename = utils.get_resource_path("styles/pushbutton.qss")
        with open(ss_filename) as ss:
            text = ss.read()
            ss = text % (
                Color.BUTTON_PRIMARY.value,
                Color.BUTTON_HOVER.value,
                Color.BUTTON_PRESSED.value
            )
            self.setStyleSheet(ss)
