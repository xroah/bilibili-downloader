from PySide6.QtWidgets import QMainWindow
from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon
from ..utils import utils
from ..MainWidget import MainWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        icon = QIcon(utils.get_resource_path("logo.ico"))
        self.setCentralWidget(MainWidget())
        self.setWindowTitle("Bilibili下载器")
        self.setWindowIcon(icon)
        self.setMinimumSize(QSize(1080, 720))
        self.setStyleSheet("background-color: rgba(0, 0, 0, .1);")
        self.show()
