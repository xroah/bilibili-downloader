from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QStackedLayout,
    QScrollArea
)
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtCore import Qt


class Panel(QWidget):
    def __init__(
            self,
            *,
            parent: QWidget = None,
            widget: QWidget
    ):
        super().__init__(parent)
        stacked = QStackedLayout(self)
        scroll_area = QScrollArea(self)
        w_layout = QVBoxLayout()
        self._layout = stacked
        self._widget = widget
        self._scroll_area = scroll_area
        self.no_content_widget = self.gen_no_content_widget()
        widget.setParent(self)
        w_layout.setAlignment(Qt.AlignTop)
        w_layout.setContentsMargins(0, 0, 0, 0)
        w_layout.setSpacing(8)
        widget.setLayout(w_layout)
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(widget)
        stacked.addWidget(self.no_content_widget)
        stacked.addWidget(scroll_area)
        stacked.setContentsMargins(0, 0, 0, 0)
        scroll_area.setStyleSheet("""
            background-color: transparent;
            border: none;
        """)

    def gen_no_content_widget(self) -> QWidget:
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
