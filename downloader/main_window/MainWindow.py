import sys
import os.path

from PySide6.QtCore import QSize, Qt, Signal
from PySide6.QtGui import (
    QCloseEvent,
    QKeyEvent,
    QResizeEvent,
    QImage,
    QBrush,
    QPalette
)
from PySide6.QtWidgets import QMainWindow, QSystemTrayIcon

from ..main_widget import MainWidget
from .Toolbar import Toolbar
from ..utils import utils, event_bus, decorators
from ..enums import EventName


@decorators.singleton
class MainWindow(QMainWindow):
    bg_sig = Signal(str)

    def __init__(self):
        super().__init__()
        self.hide_to_tray = QSystemTrayIcon.isSystemTrayAvailable()
        self.bg = utils.get_resource_path("default-bg.png")
        self._size = QSize(900, 580)
        self.setCentralWidget(MainWidget())
        self.setWindowTitle("Bilibili下载器")
        self.setMinimumSize(self._size)
        self.setWindowIcon(utils.get_icon("logo", "png"))
        self.addToolBar(Toolbar(self))
        self.setWindowFlags(
            Qt.CustomizeWindowHint |
            Qt.WindowCloseButtonHint |
            Qt.WindowMaximizeButtonHint |
            Qt.WindowMinimizeButtonHint
        )
        self.set_bg_img()
        self.show()
        event_bus.on(EventName.NEW_DOWNLOAD, self.handle_download)
        self.bg_sig.connect(self.set_bg_img)

    def set_bg_img(self, bg: str = ""):
        if bg:
            self.bg = bg

        if not self.bg or not os.path.exists(self.bg):
            return

        palette = self.palette()
        img = QImage(self.bg)
        img = img.scaled(self.size())
        brush = QBrush(img)
        palette.setBrush(QPalette.Window, brush)
        self.setPalette(palette)

    def show(self) -> None:
        self.resize(self._size)
        super().show()

    def handle_download(self, data: dict):
        print(data)

    def closeEvent(self, e: QCloseEvent) -> None:
        if self.hide_to_tray:
            self.hide()
            e.ignore()
        else:
            e.accept()

    def keyPressEvent(self, e: QKeyEvent) -> None:
        combination = e.keyCombination()
        # mac os hot key
        if (
                sys.platform == "darwin" and
                combination.keyboardModifiers() == Qt.MetaModifier
        ):
            match e.key():
                case Qt.Key_W:
                    self.close()
                case Qt.Key_M:
                    self.showMinimized()

    def resizeEvent(self, e: QResizeEvent) -> None:
        self._size = e.size()
        self.set_bg_img()
