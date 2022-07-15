import sys
from PySide6 import QtWidgets, QtCore
from downloader.MainWidget import MainWidget


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    main_win = QtWidgets.QMainWindow()
    main_win.setCentralWidget(MainWidget())
    main_win.setWindowTitle("Bilibili下载器")
    main_win.setMinimumSize(QtCore.QSize(1080, 720))
    main_win.show()

    sys.exit(app.exec())
