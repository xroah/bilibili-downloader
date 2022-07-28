import sys
from threading import Thread

from PySide6.QtCore import QCoreApplication, Qt

import downloader.qrc.Icons
from downloader.App import App
from downloader.bing_image import download_img


app: App | None = None

__version__ = "1.0.0"


def update_bg() -> None:
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
    app = App()

    t = Thread(target=update_bg)
    t.daemon = True
    t.start()

    sys.exit(app.exec())
