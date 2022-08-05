from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QStackedLayout,
    QScrollArea
)
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtCore import Qt


from ..common_widgets import ClickableWidget, CheckableItem
from ..utils import utils


class Panel(ClickableWidget):
    def __init__(
            self,
            *,
            parent: QWidget = None,
            widget: QWidget
    ):
        super().__init__(parent)
        stacked = QStackedLayout(self)
        scroll_area = QScrollArea(self)
        scroll_bar = scroll_area.verticalScrollBar()
        w_layout = QVBoxLayout()
        self._layout = stacked
        self._widget = widget
        self._scroll_area = scroll_area
        self.no_content_widget = self.gen_no_content_widget()
        widget.setParent(self)
        w_layout.setAlignment(Qt.AlignTop)
        w_layout.setContentsMargins(0, 0, 0, 0)
        w_layout.setSpacing(10)
        widget.setLayout(w_layout)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(widget)
        scroll_area.setStyleSheet("""
            background-color: transparent;
            border: none;
        """)
        scroll_bar.setStyleSheet(utils.get_style("scrollbar"))
        scroll_bar.setContextMenuPolicy(Qt.NoContextMenu)
        stacked.addWidget(self.no_content_widget)
        stacked.addWidget(scroll_area)
        stacked.setContentsMargins(0, 0, 0, 0)

    @staticmethod
    def gen_no_content_widget() -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout()
        label = QLabel()
        label_img = QImage(":/icons/empty.svg")
        hint = QLabel("无数据")
        label.setPixmap(QPixmap.fromImage(label_img))
        hint.setProperty("class", "hint")
        hint.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)
        layout.addWidget(hint)
        layout.setAlignment(Qt.AlignCenter)
        widget.setLayout(layout)

        return widget

    def find_children(self, all = True):
        children = super().findChildren(CheckableItem)

        if not all:
            children = filter(
                lambda item: item._checked,
                children
            )

        return list(children)

    def uncheck_all(self):
        checked = self.find_children(False)

        for item in checked:
            item.uncheck()

    def clickEvent(self, _):
        self.uncheck_all()
