import os

from PySide6.QtWidgets import QWidget, QLabel
from PySide6.QtCore import Qt
from PySide6.QtUiTools import QUiLoader

from ..utils import utils
from ..common_widgets import CheckableItem


class DownloadedItem(CheckableItem):
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
        loader = QUiLoader()
        widget = loader.load(utils.get_resource_path("uis/downloaded-item.ui"))
        super().__init__(
            parent=parent,
            widget=widget
        )
        deleted = not os.path.exists(path)
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

        self._ctx_menu.addAction("打开")
        self._ctx_menu.addAction("打开文件夹")
        self._ctx_menu.addAction("删除")
        self._ctx_menu.addAction("从列表中移除")
        self.setProperty(
            "class",
            f"downloaded-item{'-deleted' if deleted else ''}"
        )
        self.setProperty("name", name)
        self.setProperty("path", path)
        self.setProperty("cid", cid)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet(utils.get_style("downloaded-item"))
