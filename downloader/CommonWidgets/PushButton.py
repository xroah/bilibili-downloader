from PySide6.QtWidgets import QPushButton, QWidget
from PySide6.QtCore import Qt
from ..Color import Color


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
            self.setStyleSheet(
                """
                PushButton {
                    bg;
                    color: #fff;
                    border-radius: 3px;
                }
                PushButton:hover {
                    hover_color;
                }
            """.replace("hover_color", Color.BUTTON_HOVER.value)
                .replace("bg", Color.BUTTON_PRIMARY.value)
            )
        else:
            self.setStyleSheet("""
                PushButton {
                    border-radius: 3px;
                    background-color: #fff;
                }
                
                PushButton:hover {
                    background-color: #ddd;
                }
            """)
