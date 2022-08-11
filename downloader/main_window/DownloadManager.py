from multiprocessing import Process, Queue, Event
from threading import Thread
import time

from PySide6.QtWidgets import QPushButton, QMainWindow
from PySide6.QtCore import Signal, QObject

from ..main_widget import DownloadingPanel, DownloadedPanel
from ..main_widget.DownloadingItem import DownloadingItem
from ..main_widget.DownloadedItem import DownloadedItem
from ..db import DB
from ..utils import event_bus
from ..utils.play_ring import play_ring
from ..enums import EventName, SettingsKey, Status
from ..settings import settings
from ..download_proc import download

downloading_text = "正在下载"
downloaded_text = "已下载"


class DownloadManager(QObject):
    inited_sig = Signal()
    update_sig = Signal(dict)
    next_sig = Signal()

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
        self.downloading_items = []
        self.downloaded_items = []
        # current downloading items
        self.current_items = []
        self.downloading_btn = downloading_btn
        self.downloaded_btn = downloaded_btn
        self.downloading_panel = downloading_panel
        self.downloaded_panel = downloaded_panel
        self._window = window
        self.p: Process | None = None
        self.t: Thread | None = None
        self.q: Queue | None = None
        self.e: Event = None

        event_bus.on(EventName.NEW_DOWNLOAD, self.new_download)
        self.update_sig.connect(self.update)
        self.next_sig.connect(self.download_next)

    def init_data(self):
        with DB() as db:
            rows = db.query_all()
            self.add_downloads(rows)
            self.inited_sig.emit()

            if not settings.get(SettingsKey.IS_AUTO_DOWNLOAD):
                self.pause_all()
            else:
                self.download_first()

    def download_first(self):
        if len(self.downloading_items) and not len(self.current_items):
            for item in self.downloading_items:
                if not item.paused:
                    self.download(item)
                    break

    def download(self, item: DownloadingItem):
        if item is None:
            return

        self.e = Event()
        self.q = Queue()
        self.t = Thread(target=self.receive)
        self.t.daemon = True
        self.p = Process(
            target=download,
            kwargs={
                "event": self.e,
                "queue": self.q,
                "avid": item.property("aid"),
                "bvid": item.property("vid"),
                "cid": item.property("cid"),
                "quality": item.property("quality"),
                "name": item.property("name"),
                "album": item.property("album")
            }
        )
        self.p.daemon = True
        self.p.start()
        self.t.start()

        self.current_items.append(item)
        item.set_hint_text("正在开始")

    def update(self, data: dict):
        if not len(self.current_items):
            return

        current = self.current_items[0]

        match data["status"]:
            case Status.UPDATE:
                if "total" in data:
                    current.update_total(data["total"])

                if "speed" in data:
                    current.update_speed(data["speed"])

                if "chunk_size" in data:
                    current.update_downloaded(data["chunk_size"])
            case Status.ERROR:
                current.set_hint_text("下载错误", True)
                self.download_next()
            case Status.MERGE:
                current.set_hint_text("正在合并")
            case Status.DONE:
                if settings.get(SettingsKey.IS_PLAY_RINGTONE):
                    play_ring(self._window)

                current = self.current_items[0]
                self.current_items = []
                size = current.total
                name = current.property("name")
                cid = current.property("cid")
                path = data["video_path"]
                finish_time = time.strftime("%Y-%m-%d %H:%M:%S")

                with DB() as db:
                    db.update_finished(
                        cid=cid,
                        path=path,
                        size=size
                    )

                self.add_downloaded_item(
                    name=name,
                    cid=cid,
                    path=path,
                    size=size,
                    finish_time=finish_time
                )
                self.downloading_items.remove(current)
                current.set_hint_text("已完成")
                current.deleteLater()
                self.download_next()

    def receive(self):
        while True:
            v = self.q.get()

            if v["status"] == Status.PAUSE:
                self.p.terminate()
                self.p.join()
                self.next_sig.emit()
                break
            else:
                self.update_sig.emit(v)

                if v["status"] == Status.DONE:
                    self.p.join()
                    break

    def download_next(self):
        self.q = None
        self.p = None
        self.t = None
        self.e = None
        items = enumerate(self.downloading_items)
        next_item: DownloadingItem | None = None

        if len(self.current_items):
            self.current_items = []

        for i, item in items:
            if not item.paused and item not in self.current_items:
                next_item = item
                break

        self.download(next_item)

    def item_status_change(
            self,
            item: DownloadingItem,
            status: Status
    ):
        match status:
            case Status.PAUSE:
                if item not in self.current_items:
                    return
                self.current_items.remove(item)
                self.e.set()
            case Status.START:
                if len(self.current_items) == 0:
                    self.download(item)

    def pause_all(self):
        if self.e:
            self.e.set()

        for item in self.downloading_items:
            item.pause()

        if len(self.current_items):
            self.current_items = []

    def start_all(self):
        if not len(self.downloading_items):
            return

        for item in self.downloading_items:
            item.start()

        self.download_first()

    def add_downloaded_item(
            self,
            *,
            path: str,
            size: int,
            name: str,
            cid: int,
            finish_time: str
    ):
        item = DownloadedItem(
            path=path,
            size=size,
            name=name,
            cid=cid,
            finish_time=finish_time
        )
        self.downloaded_panel.insert_item(item)
        self.downloaded_items.append(item)
        self.update_text()

    def add_downloads(self, rows):
        for row in rows:
            name = row["name"]
            cid = row["cid"]
            if row["status"] == 0:
                item = DownloadingItem(
                    name=name,
                    cid=cid,
                    aid=row["aid"],
                    quality=row["quality"],
                    album=row["album"],
                    vid=row["vid"]
                )
                self.downloading_panel.add_item(item)
                item.status_changed.connect(self.item_status_change)
                self.downloading_items.append(item)
            else:
                self.add_downloaded_item(
                    name=name,
                    size=row["size"],
                    path=row["path"],
                    finish_time=row["finish_time"],
                    cid=cid
                )

            self.update_text()

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
        self.download_first()
