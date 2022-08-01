from typing import Callable

from PySide6.QtWidgets import QWidget, QLabel
from PySide6.QtCore import QSize

from .Dialog import Dialog


def get_label(text: str):
    label = QLabel(text)
    label.setWordWrap(True)

    return label


class MessageBox:
    size = QSize(260, 150)

    @staticmethod
    def alert(
            text: str,
            title: str = "提示",
            parent: QWidget = None
    ) -> Dialog:
        msg_box = Dialog(
            parent=parent,
            size=MessageBox.size,
            content=get_label(text),
            title=title,
            show_cancel=False
        )
        msg_box.open()

        return msg_box

    @staticmethod
    def confirm(
            text: str,
            title: str = "提示",
            parent: QWidget = None,
            on_ok: Callable = None
    ) -> Dialog:
        msg_box = Dialog(
            parent=parent,
            size=MessageBox.size,
            content=get_label(text),
            title=title,
            show_cancel=True,
            ok_callback=on_ok
        )
        msg_box.open()

        return msg_box
