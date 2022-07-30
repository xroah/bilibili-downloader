import sys
from threading import Thread
import os

from PySide6.QtCore import QCoreApplication, Qt

import downloader.qrc.Icons
from downloader.App import App
from downloader.bing_image import download_img
from downloader.utils import utils
from downloader import get_app


__version__ = "1.0.0"


def update_bg() -> None:
    app = get_app()
    if not app:
        return

    try:
        img_name = download_img()
        if img_name:
            app.main_win.set_bg_img(img_name)
    except Exception as e:
        print("======>", e)


if __name__ == "__main__":
    QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts, True)
    app = get_app()
    data_dir = utils.get_data_dir()

    if not os.path.exists(data_dir):
        os.mkdir(data_dir)

    t = Thread(target=update_bg)
    t.daemon = True
    t.start()

    sys.exit(app.exec())
