import sys
import os
from typing import cast, Callable, Union
from threading import Thread
import subprocess
import shutil

from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import (
    QFileDialog,
    QMainWindow,
    QPushButton,
    QCheckBox,
    QLabel,
    QPlainTextEdit
)
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import Qt, Signal

from ..utils import utils
from .Settings import Settings
from ..enums import SettingsKey
from ..Cookie import Cookie


class CancelException(Exception):
    pass


class SettingsDialog(QMainWindow):
    size_calculated = Signal(str)

    def __init__(self, parent: QMainWindow, on_close: Callable = None):
        super().__init__(parent)
        loader = QUiLoader()
        # calc download directory usage thread
        self.calc_thread: Thread | None = None
        # callback when terminate the calculation thread
        self.after_calc_cancel: Union[Callable, None] = None
        # should the calculation be terminated
        self.is_calc_canceled = False
        self.cookie = Cookie()
        ui_file = utils.get_resource_path("uis/settings-dialog.ui")
        widget = loader.load(ui_file)
        self.on_close = on_close
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
        self.cookie_input = cast(
            QPlainTextEdit,
            widget.findChild(QPlainTextEdit, "cookieInput")
        )
        self.settings = Settings()
        widget.setStyleSheet(utils.get_style("settings-dialog"))

        self.init_signal()
        self.init_settings()
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        self.setCentralWidget(widget)
        self.setFixedSize(650, 380)
        self.show()

    def init_settings(self):
        s = self.settings
        path = s.get(SettingsKey.DOWNLOAD_PATH)
        is_show_msg = s.get(SettingsKey.IS_SHOW_MESSAGE)
        is_play = s.get(SettingsKey.IS_PLAY_RINGTONE)
        is_monitor = s.get(SettingsKey.IS_MONITOR_CLIPBOARD)
        is_auto_download = s.get(SettingsKey.IS_AUTO_DOWNLOAD)
        self.set_checkbox_state(self.is_show_msg_checkbox, is_show_msg)
        self.set_checkbox_state(self.is_play_checkbox, is_play)
        self.set_checkbox_state(self.is_monitor_checkbox, is_monitor)
        self.set_checkbox_state(
            self.is_auto_download_checkbox,
            is_auto_download
        )
        self.cookie_input.setPlainText(self.cookie.cookie)

        if not os.path.exists(path):
            os.makedirs(path)
        self.set_path(path)

    def init_signal(self):
        self.show_btn.clicked.connect(self.get_dir)
        self.p_btn.clicked.connect(lambda: self.open_path(self.get_path()))
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
        self.size_calculated.connect(self.update_size_info)

    @staticmethod
    def set_checkbox_state(checkbox: QCheckBox, checked: bool):
        checkbox.setCheckState(Qt.Checked if checked else Qt.Unchecked)

    @staticmethod
    def get_checked(state: Qt.CheckState) -> bool:
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
        return self.settings.get(SettingsKey.DOWNLOAD_PATH)

    def get_size(self, path: str) -> float:
        size = os.path.getsize(path)
        files = os.scandir(path)

        if os.path.ismount(path):
            usage = shutil.disk_usage(path)

            return usage.used

        for f in files:
            if self.is_calc_canceled:
                self.is_calc_canceled = False
                self.calc_thread = None
                if self.after_calc_cancel:
                    self.after_calc_cancel()
                self.after_calc_cancel = None
                raise CancelException()

            f_path = os.path.join(path, f.name)
            size += os.path.getsize(f_path)
            if f.is_dir():
                size += self.get_size(f)

        return size

    def calc_size(self, path: str):
        try:
            size = self.get_size(path)
            size = utils.format_size(size)
            self.calc_thread = None
        except CancelException:
            print("Calculation canceled")
            return
        except:
            size = "未知"

        self.size_calculated.emit(size)

    def update_size_info(self, size: str):
        self.used_label.setText(size)

    def start_calc(self, path):
        if self.calc_thread:
            self.is_calc_canceled = True
            self.after_calc_cancel = lambda: self.start_calc(path)
            return

        t = Thread(target=self.calc_size, args=(path,))
        t.daemon = True
        t.start()
        self.calc_thread = t

    def set_path(self, path: str, save=False):
        self.p_btn.setText(path)
        self.used_label.setText("正在计算...")
        if save:
            self.settings.set(SettingsKey.DOWNLOAD_PATH, path)
        self.start_calc(path)

    @staticmethod
    def open_path(path):
        platform = sys.platform
        if platform == "win32":
            os.startfile(path, "open")
        else:
            subprocess.call(("open", path))

    def closeEvent(self, e: QCloseEvent) -> None:
        super().closeEvent(e)
        self.is_calc_canceled = True
        cookie = self.cookie_input.toPlainText()
        self.cookie.set(cookie)
        if self.on_close:
            self.on_close()
