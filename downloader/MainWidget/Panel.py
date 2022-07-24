from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QStackedLayout
)
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtCore import Qt

class Panel(QWidget):
    def __init__(self, parent: QWidget=None):
        super().__init__(parent)
        layout = QStackedLayout(self)
        self.no_content_widget = self.gen_no_content_widget()
        layout.addWidget(self.no_content_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)
        
        
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