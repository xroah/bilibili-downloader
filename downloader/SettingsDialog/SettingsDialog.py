from PySide6.QtWidgets import (
    QFileDialog,
    QMainWindow,
    QPushButton,
    QWidget,
    QLabel
)
from PySide6.QtUiTools import QUiLoader

import sys
import os
from typing import cast

from ..utils import utils


class SettingsDialog(QMainWindow):
    def __init__(self, parent: QMainWindow):
        super().__init__(parent)
        loader = QUiLoader()
        ui_file = utils.get_resource_path("uis/settings-dialog.ui")
        widget = loader.load(ui_file)
        show_btn = widget.findChild(QPushButton, "showFileDialogBtn")
        p_btn = cast(
            QPushButton,
            widget.findChild(QPushButton, "downloadPathBtn")
        )
        self.p_btn = p_btn
        self.used_label = cast(
            QLabel,
            widget.findChild(QLabel, "usedText")
        )
        cast(QPushButton, show_btn).clicked.connect(self.get_dir)
        p_btn.clicked.connect(self.open_download_path)
        p_btn.setText(utils.get_default_download_path())
        widget.setStyleSheet(utils.get_style("settings-dialog"))

        self.set_path(utils.get_default_download_path())
        self.setCentralWidget(widget)
        self.setFixedSize(600, 300)
        self.show()

    def get_dir(self):
        ret = QFileDialog.getExistingDirectory(
            self,
            "选择文件夹",
            self.get_path(),
            QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks
        )

        if not ret:
            return

        self.set_path(ret)

    def get_path(self):
        return self.p_btn.text().strip()

    def set_path(self, path: str):
        try:
            size = utils.get_size(path)
            size = utils.format_size(size)
        except Exception:
            size = "未知"
        self.p_btn.setText(path)
        self.used_label.setText(f"已使用: {size}")

    def open_download_path(self):
        platform = sys.platform
        path = os.path.normpath(self.get_path())
        cmd = "start" if platform == "win32" else "open"
        os.system(f"{cmd} {path}")
