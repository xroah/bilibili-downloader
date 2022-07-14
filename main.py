import sys
from PySide6 import QtWidgets, QtGui
from downloader.MainWidget import MainWidget


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MainWidget()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())
