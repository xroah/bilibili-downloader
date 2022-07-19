from PySide6.QtCore import QSize,  __version__
from PySide6.QtGui import QIcon, QMoveEvent
from PySide6.QtWidgets import QMainWindow

from ..MainWidget import MainWidget
from .Toolbar import Toolbar


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setCentralWidget(MainWidget())
        self.setWindowTitle("Bilibili下载器")
        self.setMinimumSize(QSize(800, 480))
        self.setWindowIcon(QIcon(":/logo.png"))
        self.addToolBar(Toolbar(self))
        self.show()

    def moveEvent(self, event: QMoveEvent) -> None:
        pos = event.pos()
        print(pos)
