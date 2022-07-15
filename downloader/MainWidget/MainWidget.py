import PySide6.QtWidgets as QtWidgets
from PySide6.QtCore import Qt
from ..utils import utils


class MainWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        menu_widget = QtWidgets.QListWidget()
        items = ["正在下载", "已下载"]
        for item in items:
            item = QtWidgets.QListWidgetItem(item)
            item.setTextAlignment(Qt.AlignCenter)
            menu_widget.addItem(item)

        menu_widget.setCurrentRow(0)
        text_widget = QtWidgets.QLabel(self)
        text_widget.setText("Hello world")
        self.setObjectName("mainWidget")

        content_layout = QtWidgets.QVBoxLayout()
        button = QtWidgets.QPushButton("Something")
        content_layout.addWidget(text_widget)
        content_layout.addWidget(button)
        main_widget = QtWidgets.QWidget()
        main_widget.setLayout(content_layout)

        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(menu_widget, 1)
        layout.addWidget(main_widget, 4)
        self.style().setProperty("border", "5px solid red")

        with open(utils.get_resource_path("style.qss")) as style:
            self.setStyleSheet(style.read())

        self.setGeometry(0, 0, 0, 0)
        self.setLayout(layout)
