from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QMoveEvent, QCloseEvent, QKeyEvent
from PySide6.QtWidgets import QMainWindow

from ..MainWidget import MainWidget
from .Toolbar import Toolbar
from ..utils import utils

import sys


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

    def keyPressEvent(self, e: QKeyEvent) -> None:
        combination = e.keyCombination()
        print(sys.platform, e.key() == Qt.Key_W, 
        combination.keyboardModifiers() == Qt.MetaModifier)
        # mac os meta + w
        if (
            sys.platform == "darwin" and
            e.key() == Qt.Key_W and
            combination.keyboardModifiers() == Qt.MetaModifier
        ):
            self.hide()
