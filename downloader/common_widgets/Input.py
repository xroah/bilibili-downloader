from PySide6.QtWidgets import (
    QWidget,
    QLineEdit,
    QVBoxLayout,
    QToolButton,
    QMenu
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QKeySequence, QContextMenuEvent

from ..utils import utils
from .Menu import Menu

class Input(QLineEdit):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self.clear_btn = QToolButton()
        clear_btn = self.clear_btn
        layout = QVBoxLayout()
        clear_btn.setIcon(utils.get_icon("close"))
        clear_btn.setProperty("class", "clear")
        clear_btn.setCursor(Qt.ArrowCursor)
        clear_btn.setFixedSize(20, 20)
        clear_btn.clicked.connect(self.clear)
        clear_btn.hide()

        layout.addWidget(clear_btn)
        layout.setAlignment(Qt.AlignRight)
        layout.setContentsMargins(5, 5, 5, 5)

        self.setLayout(layout)
        self.set_qss()
        self.textChanged.connect(self.text_changed_cb)

    def set_qss(self):
        qss = utils.get_resource_path("styles/input.qss")
        with open(qss) as ss:
            self.setStyleSheet(ss.read())

    def get_menu(self) -> QMenu:
        has_selected = self.hasSelectedText()
        menu = Menu(self)
        undo_action = menu.addAction("撤销")
        redo_action = menu.addAction("重做")
        menu.addSeparator()
        cut_action = menu.addAction("剪切")
        copy_action = menu.addAction("复制")
        paste_action = menu.addAction("粘贴")
        del_action = menu.addAction("删除")
        menu.addSeparator()
        select_action = menu.addAction("全选")
        undo_action.setShortcut(QKeySequence.Undo)
        undo_action.setEnabled(self.isUndoAvailable())
        undo_action.triggered.connect(self.undo)
        redo_action.setShortcut(QKeySequence.Redo)
        redo_action.setEnabled(self.isRedoAvailable())
        redo_action.triggered.connect(self.redo)
        cut_action.setEnabled(has_selected)
        cut_action.setShortcut(QKeySequence.Cut)
        cut_action.triggered.connect(self.cut)
        copy_action.setEnabled(has_selected)
        copy_action.setShortcut(QKeySequence.Copy)
        copy_action.triggered.connect(self.copy)
        paste_action.setShortcut(QKeySequence.Paste)
        paste_action.triggered.connect(self.paste)
        del_action.setEnabled(has_selected)
        del_action.triggered.connect(self.backspace)
        select_action.setShortcut(QKeySequence.SelectAll)
        select_action.setEnabled(bool(self.text()))
        select_action.triggered.connect(self.selectAll)

        menu.setProperty("class", "contextmenu")
        menu.setStyleSheet(utils.get_style("menu"))
        self.setStyleSheet(utils.get_style("input"))

        return menu

    def text_changed_cb(self):
        if self.text():
            self.clear_btn.show()
        else:
            self.clear_btn.hide()

    def contextMenuEvent(self, e: QContextMenuEvent) -> None:
        menu = self.get_menu()
        menu.exec(e.globalPos())
