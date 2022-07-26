from PySide6.QtWidgets import QMessageBox, QWidget


class MessageBox:
    @staticmethod
    def alert(
            text: str, *,
            title: str = "提示",
            show_icon: bool = True,
            parent: QWidget = None
    ) -> QMessageBox:
        msg_box = QMessageBox(text=text, parent=parent)
        msg_box.setWindowTitle(title)
        msg_box.addButton("确定", QMessageBox.AcceptRole)
        msg_box.setStyleSheet("""
            QLabel {
                padding: 5px 0;
            }
        """)
        if show_icon:
            msg_box.setIcon(QMessageBox.Information)
        msg_box.exec()

        return msg_box
