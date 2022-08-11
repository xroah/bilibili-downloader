from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QMouseEvent
from PySide6.QtCore import Qt, QEvent, QTimer


class ClickableWidget(QWidget):
    def __init__(self, parent: any = None):
        super().__init__(parent)
        self._timer: QTimer | None = None
        self._mouse_pressed = False
        self._mouse_entered = False

    def _click(self, modifier: Qt.KeyboardModifiers):
        self._timer = None
        self._mouse_pressed = False
        self.click_event(modifier)

    def mousePressEvent(self, e: QMouseEvent) -> None:
        self._mouse_pressed = True

    def mouseReleaseEvent(self, e: QMouseEvent):
        # click event
        if (
                e.button() == Qt.LeftButton and
                self._mouse_pressed and
                self._mouse_entered
        ):
            self._click(e.modifiers())

    def enterEvent(self, e: QEvent):
        self._mouse_entered = True

    def leaveEvent(self, e: QEvent):
        self._mouse_entered = False

    def click_event(self, modifier):
        pass
