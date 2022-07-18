from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtWidgets import (
    QMainWindow,
    QToolBar,
    QToolButton,
    QWidget,
    QSizePolicy
)

from ..MainWidget import MainWidget
import downloader.QRC.Icons


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.add_btn = QToolButton()
        self.menu_btn = QToolButton()
        self.setCentralWidget(MainWidget())
        self.setWindowTitle("Bilibili下载器")
        self.setMinimumSize(QSize(1080, 720))
        self.setWindowIcon(QIcon(QPixmap(":/logo.png")))
        self.add_btn.setIcon(QIcon(QPixmap(":/plus.png")))
        self.menu_btn.setIcon(QIcon(QPixmap(":/menu.png")))
        self.set_toolbar()
        self.show()

    def set_menu(self, btn: QToolButton):
        pass

    def set_toolbar(self):
        toolbar = QToolBar(self)
        toolbar.setMovable(False)
        placeholder = QWidget()
        placeholder.setProperty("class", "placeholder")
        placeholder.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        toolbar.setObjectName("toolbar")
        toolbar.addWidget(self.add_btn)
        toolbar.addWidget(placeholder)
        toolbar.addWidget(self.menu_btn)
        toolbar.setStyleSheet("""
            QToolBar#toolbar {
                padding: 5px;
                border-bottom: 1px solid rgba(0, 0, 0, .1);
                background-color: #fff;
            }
            
            .placeholder {
                background-color: transparent;
            }
            
            QToolButton {
                width: 24px;
                height: 24px;
            }
            
            
        """)

        self.addToolBar(toolbar)
