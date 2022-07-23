import sys
from threading import Thread

import downloader.QRC.Icons
import downloader.QRC.Styles
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
            app.main_win.set_bg_path(img_name)
            app.main_win.set_bg_img()
    except Exception as e:
        print(e)

if __name__ == "__main__":
    app = App()
    
    t1 = Thread(target=update_bg)
    t1.daemon = True
    t1.start()
        
    sys.exit(app.exec())
