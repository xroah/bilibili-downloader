from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QStackedLayout,
    QScrollArea
)
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtCore import Qt, QObject, Signal

from ..common_widgets import ClickableWidget
from .CheckableItem import CheckableItem
from ..utils import utils


class Panel(ClickableWidget):
    del_sig = Signal(QObject)
    rm_sig = Signal(QObject)
    toggle_sig = Signal(QObject)

    def __init__(
            self,
            *,
            parent: QWidget = None,
            widget: QWidget = None
    ):
        super().__init__(parent)
        stacked = QStackedLayout(self)
        scroll_area = QScrollArea(self)
        scroll_bar = scroll_area.verticalScrollBar()
        self._layout = stacked
        self._widget: QWidget | None = widget
        self._scroll_area = scroll_area
        self._no_content_widget = self.gen_no_content_widget()
        self._stacked = stacked
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("""
            border: none;
            background-color: transparent;
        """)
        scroll_bar.setStyleSheet(utils.get_style("scrollbar"))
        scroll_bar.setContextMenuPolicy(Qt.NoContextMenu)
        stacked.addWidget(self._no_content_widget)
        stacked.addWidget(scroll_area)
        stacked.setContentsMargins(0, 0, 0, 0)
        self.set_widget(widget)

    def set_widget(self, widget: QWidget = None):
        if not widget:
            return

        w_layout = QVBoxLayout()
        self._widget = widget
        widget.setParent(self)
        w_layout.setAlignment(Qt.AlignTop)
        w_layout.setContentsMargins(0, 0, 0, 10)
        w_layout.setSpacing(10)
        widget.setLayout(w_layout)
        self._scroll_area.setWidget(widget)

    def set_current_index(self, i: int):
        self._layout.setCurrentIndex(i)

    def get_current_index(self):
        return self._layout.currentIndex()

    @staticmethod
    def gen_no_content_widget() -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout()
        label = QLabel()
        label_img = QImage(":/icons/empty.svg")
        hint = QLabel("无数据")
        label.setPixmap(QPixmap.fromImage(label_img))
        hint.setProperty("class", "no-data-text")
        hint.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)
        layout.addWidget(hint)
        layout.setAlignment(Qt.AlignCenter)
        widget.setLayout(layout)

        return widget

    def find_children(self, get_all=True):
        children = super().findChildren(CheckableItem)

        if not get_all:
            children = filter(
                lambda item: item.checked,
                children
            )

        return list(children)

    def uncheck_all(self):
        checked = self.find_children(False)

        for item in checked:
            item.uncheck()

    def check_all(self):
        items = self.find_children()

        for item in items:
            item.check()

    def click_event(self, _):
        self.uncheck_all()
