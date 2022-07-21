import sys
from PySide6 import QtWidgets
from downloader.MainWindow import MainWindow
import downloader.QRC.Icons
import downloader.QRC.Styles

__version__ = "1.0.0"

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    main_win = MainWindow()

    sys.exit(app.exec())
