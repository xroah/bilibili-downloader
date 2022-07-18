from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QIcon, QPixmap, QAction
from PySide6.QtWidgets import (
    QMainWindow,
    QToolBar,
    QToolButton,
    QWidget,
    QSizePolicy,
    QMenu
)
import sys

from ..MainWidget import MainWidget
from ..utils import utils
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
        self.set_menu(self.menu_btn)
        self.show()

    def set_menu(self, btn: QToolButton):
        menu = QMenu(self)
        about_action = menu.addAction("关于")
        exit_action = menu.addAction("退出")
        about_action.triggered.connect(self.about_action)
        exit_action.triggered.connect(self.exit_action)
        btn.setPopupMode(QToolButton.InstantPopup)
        btn.setMenu(menu)
        menu.setStyleSheet("""
            QMenu {
                padding: 0;
                border-radius: 5px;
                border: 1px solid #f0f0f0; 
                background-color: #fff;
            }
            
            QMenu::item {
                margin: 0;
                min-width: 150px;
                padding: 10px;
            }
            
            QMenu::item:selected {
                color: #fff;
                background-color: rgba(13, 110, 253, .6);
            }
        """)

    def about_action(self):
        print("about")

    def exit_action(self):
        sys.exit(0)

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
        toolbar.setContextMenuPolicy(Qt.PreventContextMenu)

        with open(utils.get_resource_path("styles/toolbar.qss")) as ss:
            toolbar.setStyleSheet(ss.read())

        self.addToolBar(toolbar)
