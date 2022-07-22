import sys
from multiprocessing import Process

from downloader.MainWindow import MainWindow
import downloader.QRC.Icons
import downloader.QRC.Styles
from downloader.App import App
from downloader.BingImage import download_img

__version__ = "1.0.0"

def download_callback(img_name: str, app: App) -> None:
    print(img_name, app, "<<<<<")
    try:
        app.main_win.set_bg_path(img_name)
        app.main_win.set_bg_img(img_name)
    except:
        pass


if __name__ == "__main__":
    app = App()
    
    try:
        p = Process(target=download_img, args=(download_callback, ))
        p.start()
    except Exception as e:
        print(e)

    sys.exit(app.exec())
