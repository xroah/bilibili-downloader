from PySide6.QtWidgets import (
    QFileDialog,
    QMainWindow,
    QPushButton,
    QWidget,
    QLabel
)
from PySide6.QtUiTools import QUiLoader

import subprocess
import sys
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

        self.setCentralWidget(widget)
        self.setFixedSize(500, 300)
        self.show()

    def get_dir(self):
        ret = QFileDialog.getExistingDirectory(
            self,
            "选择文件夹",
            "",
            QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks
        )
        print(ret)

    def open_download_path(self):
        platform = sys.platform
        c = self.findChild(QPushButton, "downloadPathBtn")
        btn: QPushButton = cast(QPushButton, c)
        text = btn.text().strip()
        # subprocess.run(["start" if platform == "win32" else "open"])
        print(text)
