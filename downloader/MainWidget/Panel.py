from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QStackedLayout,
    QProgressBar
)
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtCore import Qt

from .DownloadingItem import DownloadingItem


class Panel(QWidget):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        layout = QStackedLayout(self)
        self.no_content_widget = self.gen_no_content_widget()
        layout.addWidget(self.no_content_widget)
        layout.addWidget(DownloadingItem(self))
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setCurrentIndex(1)

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

    def get_list(self) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout()
        pb = QProgressBar()
        pb.setTextVisible(False)
        pb.setStyleSheet("""
            QProgressBar {
                border: 2px solid grey;
                border-radius: 5px;
            }

            QProgressBar::chunk {
                background-color: #05B8CC;
                width: 20px;
            }
        """)
        pb.setValue(60)
        widget.setLayout(layout)
        layout.addWidget(pb)

        return widget
