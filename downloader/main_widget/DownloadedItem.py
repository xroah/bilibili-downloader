import os
from pathlib import PurePath

from PySide6.QtWidgets import QWidget, QLabel
from PySide6.QtCore import Qt
from PySide6.QtGui import QMouseEvent

from ..utils import utils
from .Item import Item


class DownloadedItem(Item):
    def __init__(
            self,
            parent: QWidget = None,
            *,
            path: str,
            size: int,
            name: str,
            cid: int,
            finish_time: str
    ):
        super().__init__(
            parent=parent,
            ui="downloaded-item"
        )
        deleted = not os.path.exists(path)
        widget = self._widget
        self.deleted = deleted
        self.name_label = utils.get_child(widget, QLabel, "videoName")
        self.path_label = utils.get_child(widget, QLabel, "videoPath")
        self.size_label = utils.get_child(widget, QLabel, "videoSize")
        self.time_label = utils.get_child(widget, QLabel, "videoTime")

        if not deleted:
            label = utils.get_child(widget, QLabel, "deletedText")
            layout = widget.layout()
            if label and layout:
                layout.removeWidget(label)
                label.deleteLater()

        self.name_label.setText(name)
        self.path_label.setText(path)
        self.size_label.setText(utils.format_size(size))
        self.time_label.setText(finish_time)

        self.setProperty(
            "class",
            f"downloaded-item{'-deleted' if deleted else ''}"
        )
        self.setProperty("name", name)
        self.setProperty("path", path)
        self.setProperty("cid", cid)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet(utils.get_style("downloaded-item"))
        self.init_menu()

    def init_menu(self):
        open_action = self._ctx_menu.addAction("打开")
        open_dir_action = self._ctx_menu.addAction("打开所在文件夹")
        del_action = self._ctx_menu.addAction("删除")
        rm_action = self._ctx_menu.addAction("从列表中移除")

        open_action.triggered.connect(self.open_file)
        open_dir_action.triggered.connect(self.open_dir)
        del_action.triggered.connect(self.delete)
        rm_action.triggered.connect(
            lambda: self._parent.rm_sig.emit(self)
        )

    def delete_later(self, remove_file=False):
        if remove_file:
            path = self.property("path")
            try:
                os.unlink(path)
            except:
                pass
        super().deleteLater()

    def open_dir(self):
        if self.deleted:
            return

        path = PurePath(self.property("path"))
        utils.open_path(str(path.parent))

    def open_file(self):
        if self.deleted:
            return

        utils.open_path(self.property("path"))

    def mouseDoubleClickEvent(self, event: QMouseEvent) -> None:
        self.open_file()
