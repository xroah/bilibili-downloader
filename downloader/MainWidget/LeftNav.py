from PySide6.QtWidgets import (
    QPushButton,
    QWidget,
    QVBoxLayout
)
from PySide6.QtCore import Qt, Signal
from typing import Any

from ..Enums import Color
from ..utils import utils


class LeftNav(QWidget):
    changed = Signal(QPushButton)

    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self.current: QPushButton | None = None
        layout = QVBoxLayout()
        self.downloading_btn = self.create_btn(
            "downloading-btn",
            "正在下载",
            self.downloading_btn_press
        )
        self.downloaded_btn = self.create_btn(
            "downloaded-btn",
            "已下载",
            self.downloaded_btn_press
        )
        layout.addWidget(self.downloading_btn)
        layout.addWidget(self.downloaded_btn)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addStretch()
        layout.setSpacing(0)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setLayout(layout)
        self.setStyleSheet(utils.get_style("left-nav"))
        self.switch_tab(self.downloading_btn)

    def create_btn(
            self,
            classname: str,
            text: str,
            press_cb: Any
    ) -> QPushButton:
        btn = QPushButton(parent=self, text=text)
        btn.setProperty("class", classname)
        btn.setCursor(Qt.PointingHandCursor)
        btn.pressed.connect(press_cb)

        return btn

    def switch_tab(self, btn: QPushButton):
        if self.current:
            if self.current == btn:
                return

            self.current.setStyleSheet("")

        self.current = btn
        btn.setStyleSheet(f"""
            {Color.BUTTON_PRESSED.value};
            color: #fff; 
        """)
        self.changed.emit(btn)

    def downloading_btn_press(self):
        print("downloading btn")
        self.switch_tab(self.downloading_btn)

    def downloaded_btn_press(self):
        print("downloaded btn")
        self.switch_tab(self.downloaded_btn)
