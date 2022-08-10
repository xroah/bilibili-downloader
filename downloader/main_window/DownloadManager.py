from threading import Thread

from PySide6.QtWidgets import QPushButton, QMainWindow, QWidget
from PySide6.QtCore import Signal, QObject

from ..main_widget import DownloadingPanel, DownloadedPanel
from ..main_widget.DownloadingItem import DownloadingItem
from ..db import DB
from ..utils import event_bus
from ..enums import EventName

downloading_text = "正在下载"
downloaded_text = "已下载"


class DownloadManager(QObject):
    def __init__(
            self,
            *,
            window: QMainWindow,
            downloading_btn: QPushButton,
            downloaded_btn: QPushButton,
            downloading_panel: DownloadingPanel,
            downloaded_panel: DownloadedPanel
    ):
        super().__init__()
        self.currents = []
        self.downloading_btn = downloading_btn
        self.downloaded_btn = downloaded_btn
        self.downloading_panel = downloading_panel
        self.downloaded_panel = downloaded_panel
        self.downloading = 0
        self.downloaded = 0
        self._window = window

        event_bus.on(EventName.NEW_DOWNLOAD, self.new_download)
        self.init_data()

    def init_data(self):
        with DB() as db:
            rows = db.query_all()
            self.add_downloads(rows)

    def add_items(
            self,
            downloading_items,
            downloaded_items
    ):
        for item in downloading_items:
            self.downloading_panel.add_item(item)
            self.downloading += 1

        self.update_text()

    def add_downloads(self, rows):
        downloading_items = []
        downloaded_items = []

        for row in rows:
            if row["status"] == 0:
                item = DownloadingItem(
                    name=row["name"],
                    cid=row["cid"],
                    aid=row["aid"],
                    quality=row["quality"],
                    album=row["album"],
                    vid=row["vid"]
                )
                downloading_items.append(item)

        self.add_items(downloading_items, downloaded_items)

    def update_downloading_text(self):
        self.downloading_btn.setText(
            f"{downloading_text}({self.downloading})"
        )

    def update_downloaded_text(self):
        self.downloaded_btn.setText(
            f"{downloaded_text}({self.downloaded})"
        )

    def update_text(self):
        self.update_downloading_text()
        self.update_downloaded_text()

    def new_download(self, data):
        pass
