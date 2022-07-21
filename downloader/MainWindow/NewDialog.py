from ..CommonWidgets import Dialog
from ..utils import utils
from ..CommonWidgets import Input

from PySide6.QtCore import QSize
from PySide6.QtWidgets import (
    QLabel,
    QMainWindow,
    QWidget,
    QVBoxLayout
)


class NewDialog:
    def __init__(self, window: QMainWindow):
        self.dialog = Dialog(
            title="新建下载",
            parent=window,
            show_cancel=True,
            size=QSize(420, 150),
            close_on_enter=False
        )
        self.init()

    def init(self):
        content = QWidget()
        layout = QVBoxLayout(content)
        input_ = Input(content)
        input_.setFrame(False)
        input_.setProperty("class", "input")

        layout.addWidget(QLabel("输入BV号/视频地址/搜索内容"))
        layout.addWidget(input_)
        content.setProperty("class", "new-dialog")
        content.setLayout(layout)
        content.setStyleSheet(utils.get_style("new-dialog"))

        self.dialog.shown.connect(lambda: input_.setFocus())
        self.dialog.set_content(content)

    def open(self):
        self.dialog.open_()

