from PySide6.QtWidgets import (
    QFileDialog,
    QMainWindow,
    QPushButton,
    QCheckBox,
    QLabel
)
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import Qt

import sys
import os
from typing import cast

from ..utils import utils
from .Settings import Settings
from ..enums import SettingsKey


class SettingsDialog(QMainWindow):
    def __init__(self, parent: QMainWindow):
        super().__init__(parent)
        loader = QUiLoader()
        ui_file = utils.get_resource_path("uis/settings-dialog.ui")
        widget = loader.load(ui_file)
        self.show_btn = cast(
            QPushButton,
            widget.findChild(QPushButton, "showFileDialogBtn")
        )
        self.p_btn = cast(
            QPushButton,
            widget.findChild(QPushButton, "downloadPathBtn")
        )
        self.used_label = cast(
            QLabel,
            widget.findChild(QLabel, "usedText")
        )
        self.is_show_msg_checkbox = cast(
            QCheckBox,
            widget.findChild(QCheckBox, "isShowMessage")
        )
        self.is_play_checkbox = cast(
            QCheckBox,
            widget.findChild(QCheckBox, "isPlayRingtone")
        )
        self.is_monitor_checkbox = cast(
            QCheckBox,
            widget.findChild(QCheckBox, "isMonitorClipboard")
        )
        self.is_auto_download_checkbox = cast(
            QCheckBox,
            widget.findChild(QCheckBox, "isAutoDownload")
        )
        self.settings = Settings()
        self.show_btn.setStyleSheet(utils.get_style("pushbutton"))
        widget.setStyleSheet(utils.get_style("settings-dialog"))

        self.init_signal()
        self.init_settings()
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        self.setCentralWidget(widget)
        self.setFixedSize(600, 300)
        self.show()

    def init_settings(self):
        s = self.settings
        path = s.get(SettingsKey.DOWNLOAD_PATH)
        is_show_msg = s.get(SettingsKey.IS_SHOW_MESSAGE)
        is_play = s.get(SettingsKey.IS_PLAY_RINGTONE)
        is_monitor = s.get(SettingsKey.IS_MONITOR_CLIPBOARD)
        is_auto_download = s.get(SettingsKey.IS_AUTO_DOWNLOAD)
        self.setCheckboxState(self.is_show_msg_checkbox, is_show_msg)
        self.setCheckboxState(self.is_play_checkbox, is_play)
        self.setCheckboxState(self.is_monitor_checkbox, is_monitor)
        self.setCheckboxState(self.is_auto_download_checkbox, is_auto_download)

        if not os.path.exists(path):
            os.makedirs(path)
        self.set_path(path)

    def init_signal(self):
        self.show_btn.clicked.connect(self.get_dir)
        self.p_btn.clicked.connect(self.open_download_path)
        self.is_show_msg_checkbox.stateChanged.connect(
            lambda s: self.handle_change(SettingsKey.IS_SHOW_MESSAGE, s)
        )
        self.is_play_checkbox.stateChanged.connect(
            lambda s: self.handle_change(SettingsKey.IS_PLAY_RINGTONE, s)
        )
        self.is_monitor_checkbox.stateChanged.connect(
            lambda s: self.handle_change(SettingsKey.IS_MONITOR_CLIPBOARD, s)
        )
        self.is_auto_download_checkbox.stateChanged.connect(
            lambda s: self.handle_change(SettingsKey.IS_AUTO_DOWNLOAD, s)
        )

    def setCheckboxState(self, checkbox: QCheckBox, checked: bool):
        checkbox.setCheckState(Qt.Checked if checked else Qt.Unchecked)

    def get_checked(self, state: Qt.CheckState) -> bool:
        return state == Qt.Checked

    def handle_change(self, prop: str | SettingsKey, state: Qt.CheckState):
        self.settings.set(prop, self.get_checked(state))

    def get_dir(self):
        ret = QFileDialog.getExistingDirectory(
            self,
            "选择文件夹",
            self.get_path(),
            QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks
        )

        if not ret or ret == self.settings.get(SettingsKey.DOWNLOAD_PATH):
            return

        self.set_path(ret, True)

    def get_path(self):
        return self.p_btn.text().strip()

    def set_path(self, path: str, save=False):
        try:
            size = utils.get_size(path)
            size = utils.format_size(size)
        except Exception:
            size = "未知"
        self.p_btn.setText(path)
        self.used_label.setText(f"已使用: {size}")

        if save:
            self.settings.set(SettingsKey.DOWNLOAD_PATH, path)

    def open_download_path(self):
        platform = sys.platform
        path = os.path.normpath(self.get_path())
        cmd = "start" if platform == "win32" else "open"
        os.system(f"{cmd} {path}")
