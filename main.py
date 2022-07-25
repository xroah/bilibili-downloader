import sys
from threading import Thread

import downloader.QRC.Icons
from downloader.App import App
from downloader.BingImage import download_img

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
    app = App()

    t = Thread(target=update_bg)
    t.daemon = True
    t.start()

    sys.exit(app.exec())
