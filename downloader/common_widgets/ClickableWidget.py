from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QMouseEvent
from PySide6.QtCore import Qt, QEvent, QTimer


class ClickableWidget(QWidget):
    def __init__(self,parent: QWidget = None):
        super().__init__(parent)
        self._timer: QTimer | None = None
        self._mouse_pressed = False
        self._mouse_entered = False

    def _click(self, modifier: Qt.KeyboardModifiers):
        self._timer = None
        self._mouse_pressed = False
        self.clickEvent(modifier)

    def clickEvent(self, modifier: Qt.KeyboardModifiers):
        pass

    def dblClickEvent(self):
        pass

    def mousePressEvent(self, e: QMouseEvent) -> None:
        self._mouse_pressed = True

    def mouseReleaseEvent(self, e: QMouseEvent):
        # click event
        if (
            e.button() == Qt.LeftButton and
            self._mouse_pressed and
            self._mouse_entered
        ):
            modifier = e.modifiers()
            if self._timer:
                # double click
                self._timer.stop()
                self._timer = None
                self.dblClickEvent()
            else:
                self._timer = QTimer()
                self._timer.timeout.connect(
                    lambda: self._click(modifier)
                )
                self._timer.start(200)

    def enterEvent(self, e: QEvent):
        self._mouse_entered = True
    
    def leaveEvent(self, e: QEvent):
        self._mouse_entered = False
