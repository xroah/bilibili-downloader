from PySide6.QtCore import QSize
from PySide6.QtGui import QMoveEvent, QCloseEvent
from PySide6.QtWidgets import QMainWindow

from ..MainWidget import MainWidget
from .Toolbar import Toolbar
from ..utils import utils


class MainWindow(QMainWindow):
    def __init__(self, hide_to_tray=True):
        super().__init__()
        self.hide_to_tray = hide_to_tray
        self.setCentralWidget(MainWidget())
        self.setWindowTitle("Bilibili下载器")
        self.setMinimumSize(QSize(800, 480))
        self.setWindowIcon(utils.get_icon("logo"))
        self.addToolBar(Toolbar(self))
        self.show()

    def moveEvent(self, event: QMoveEvent) -> None:
        super().moveEvent(event)
        pos = event.pos()
        print(pos)

    def closeEvent(self, e: QCloseEvent) -> None:
        if self.hide_to_tray:
            self.hide()
            e.ignore()
        else:
            e.accept()
