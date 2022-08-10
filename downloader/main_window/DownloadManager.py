from PySide6.QtWidgets import QPushButton, QMainWindow
from PySide6.QtCore import Signal, QObject, QThreadPool

from ..main_widget import DownloadingPanel, DownloadedPanel
from ..main_widget.DownloadingItem import DownloadingItem
from ..db import DB
from ..utils import event_bus
from ..enums import EventName, SettingsKey, Status
from ..settings import settings

downloading_text = "正在下载"
downloaded_text = "已下载"


class DownloadManager(QObject):
    inited_sig = Signal()

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
        self.downloading_items = []
        self.downloaded_items = []
        # current downloading items
        self.current_items = []
        self.downloading_btn = downloading_btn
        self.downloaded_btn = downloaded_btn
        self.downloading_panel = downloading_panel
        self.downloaded_panel = downloaded_panel
        self._window = window

        event_bus.on(EventName.NEW_DOWNLOAD, self.new_download)

    def init_data(self):
        with DB() as db:
            rows = db.query_all()
            self.add_downloads(rows)
            self.inited_sig.emit()

            if not settings.get(SettingsKey.IS_AUTO_DOWNLOAD):
                self.pause_all()
            else:
                self.download(self.downloading_items[0])

    def download(self, item: DownloadingItem):
        if item is None:
            return

        self.current_items.append(item)
        item.set_hint_text("正在开始")

    def item_status_change(
            self,
            item: DownloadingItem,
            status: Status
    ):
        match status:
            case Status.PAUSE:
                if item not in self.current_items:
                    return

                items = enumerate(self.downloading_items)
                next_item: DownloadingItem | None = None

                for i, item_ in items:
                    if item is not item_ and not item_.paused:
                        next_item = item_
                        break

                self.current_items.remove(item)
                self.download(next_item)
            case Status.START:
                if len(self.current_items) == 0:
                    self.download(item)

    def pause_all(self):
        for item in self.downloading_items:
            item.pause()

        if len(self.current_items):
            self.current_items = []

    def start_all(self):
        if not len(self.downloading_items):
            return

        for item in self.downloading_items:
            item.start()

        if not len(self.current_items):
            self.download(self.downloading_items[0])

    def add_items(
            self,
            downloading_items,
            downloaded_items
    ):
        self.downloading_items = [
            *self.downloading_items,
            *downloading_items
        ]

        for item in downloading_items:
            self.downloading_panel.add_item(item)
            item.status_changed.connect(self.item_status_change)

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
            f"{downloading_text}({len(self.downloading_items)})"
        )

    def update_downloaded_text(self):
        self.downloaded_btn.setText(
            f"{downloaded_text}({len(self.downloaded_items)})"
        )

    def update_text(self):
        self.update_downloading_text()
        self.update_downloaded_text()

    def new_download(self, data):
        self.add_downloads(data)
