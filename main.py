import sys
from threading import Thread
import os

from PySide6.QtCore import QCoreApplication, Qt

import downloader.qrc.Icons
from downloader.bing_image import (
    download_img,
    check,
    get_img_path
)
from downloader.utils import utils
from downloader.App import App
from downloader.db import db


__version__ = "1.0.0"


def update_bg() -> None:
    _app = App()

    try:
        name = download_img()
        if name:
            _app.main_win.bg_sig.emit(name)
    except Exception as e:
        print("======>", e)


if __name__ == "__main__":
    QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts, True)
    app = App()
    data_dir = utils.get_data_dir()

    if not os.path.exists(data_dir):
        os.mkdir(data_dir)

    img_name, img_path = get_img_path()

    if check(img_name):
        app.main_win.set_bg_img(img_path)
    else:
        t = Thread(target=update_bg)
        t.daemon = True
        t.start()

    db.create_table()
    sys.exit(app.exec())
