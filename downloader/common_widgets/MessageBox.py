from typing import Callable

from PySide6.QtWidgets import (
    QMessageBox,
    QWidget,
    QPushButton
)


class MessageBox:
    @staticmethod
    def alert(
            text: str,
            *,
            title: str = "提示",
            show_icon: bool = True,
            parent: QWidget = None
    ) -> QMessageBox:
        msg_box = QMessageBox(text=text, parent=parent)
        # title in constructor raises 'title()' is not a Qt property or a signal
        msg_box.addButton("确定", QMessageBox.AcceptRole)
        msg_box.setWindowTitle(title)
        if show_icon:
            msg_box.setIcon(QMessageBox.Information)
        msg_box.exec()

        return msg_box

    @staticmethod
    def confirm(
            text: str,
            *,
            title: str = "提示",
            show_icon: bool = True,
            parent: QWidget = None,
            on_ok: Callable = None
    ):
        msg_box = QMessageBox(text=text,parent=parent)
        cancel_btn = QPushButton("取消")
        ok_btn = QPushButton("确定")
        if on_ok:
            ok_btn.clicked.connect(on_ok)
        msg_box.addButton(cancel_btn, QMessageBox.RejectRole)
        msg_box.addButton(ok_btn, QMessageBox.AcceptRole)
        msg_box.setWindowTitle(title)
        if show_icon:
            msg_box.setIcon(QMessageBox.Question)
        msg_box.exec()

        return msg_box
