from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QMainWindow,
    QToolBar,
    QToolButton,
    QWidget,
    QSizePolicy
)

from ..MainWidget import MainWidget
from ..utils import utils


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        icon = QIcon(utils.get_resource_path("logo.ico"))
        self.setCentralWidget(MainWidget())
        self.setWindowTitle("Bilibili下载器")
        self.setWindowIcon(icon)
        self.setMinimumSize(QSize(1080, 720))
        self.set_toolbar()
        self.show()

    def set_toolbar(self):
        toolbar = QToolBar(self)
        toolbar.setMovable(False)
        add_btn = QToolButton()
        menu_btn = QToolButton()
        placeholder = QWidget()
        placeholder.setProperty("class", "placeholder")
        placeholder.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        toolbar.setObjectName("toolbar")
        toolbar.addWidget(add_btn)
        toolbar.addWidget(placeholder)
        toolbar.addWidget(menu_btn)
        toolbar.setStyleSheet("""
            QToolBar#toolbar {
                padding: 10px;
                border-bottom: 1px solid rgba(0, 0, 0, .1);
                background-color: #fff;
            }
            
            .placeholder {
                background-color: transparent;
            }
            
            QToolButton {
                width: 24px;
                height: 24px;
                background-color: blue;
            }
            
            QToolButton:hover {
                background-color: red;
            }
        """)

        self.addToolBar(toolbar)
