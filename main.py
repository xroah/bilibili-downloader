import sys
from PySide6 import QtWidgets
from downloader.MainWindow import MainWindow


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    main_win = MainWindow()

    sys.exit(app.exec())
