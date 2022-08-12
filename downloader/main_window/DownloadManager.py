import os
from multiprocessing import Process, Queue, Event
from threading import Thread
import time

from PySide6.QtWidgets import QPushButton, QMainWindow
from PySide6.QtCore import Signal, QObject

from ..common_widgets import MessageBox
from ..main_widget import (
    DownloadingPanel,
    DownloadedPanel,
    DownloadedItem,
    DownloadingItem
)
from ..db import DB
from ..utils import event_bus
from ..utils.play_ring import play_ring
from ..enums import EventName, SettingsKey, Status
from ..settings import settings
from ..download import download

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
        self.downloading_panel.del_sig.connect(self.delete_downloading)
        self.downloading_panel.toggle_sig.connect(
            self.toggle_downloading
        )
        self.downloaded_panel.del_sig.connect(self.delete_downloaded)
        self.downloaded_panel.rm_sig.connect(self.remove_downloaded)

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
        self.t = Thread(target=self.receive, args=(self.q,))
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
                "album": item.property("album"),
                "has_size": item.total > 0
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
                if self.p:
                    self.p.join()

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
                    db.update_finished(cid=cid, path=path)

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
                self.update_text()

    def receive(self, q: Queue):
        while True:
            v = q.get()

            if v["status"] == Status.PAUSE:
                if self.p:
                    self.p.terminate()
                    self.p.join()

                self.next_sig.emit()
                break
            else:
                self.update_sig.emit(v)

                if v["status"] == Status.DONE:
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
            if not item.paused:
                next_item = item
                break

        self.download(next_item)

    def stop(self):
        if self.e:
            self.e.set()

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
                self.stop()
            case Status.START:
                if len(self.current_items) == 0:
                    self.download(item)

    def delete_items(
            self,
            cids,
            items,
            is_downloading,
            delete_file=False
    ):
        with DB() as db:
            db.delete_rows(tuple(cids))

        for item in items:
            if is_downloading:
                if item in self.downloading_items:
                    item.delete_later()
                    self.downloading_items.remove(item)
            else:
                if item in self.downloaded_items:
                    self.downloaded_items.remove(item)
                    item.delete_later(delete_file)

        self.update_text()

    def handle_downloading(self, t: str, item: DownloadingItem):
        checked = self.downloading_panel.find_children(False)
        downloading = False
        paused = item.paused
        cids = []

        if (
                len(self.current_items) and
                self.current_items[0] in checked
        ):
            self.stop()
            downloading = True

        for c in checked:
            match t:
                case "delete":
                    cids.append(str(c.property("cid")))
                case "toggle":
                    if paused:
                        c.start()
                    else:
                        c.pause()

        if t == "delete":
            self.delete_items(cids, checked, True)

        # if downloading, download next will be called by the update thread
        if not downloading:
            self.download_next()

    def toggle_downloading(self, item: DownloadingItem):
        self.handle_downloading("toggle", item)

    def delete_downloading(self, item: DownloadingItem):
        self.handle_downloading("delete", item)

    def handle_downloaded(self, t: str):
        checked = self.downloaded_panel.find_children(False)
        cids = []

        for c in checked:
            cids.append(str(c.property("cid")))

        match t:
            case "delete":
                MessageBox.confirm(
                    text="确定要删除选中的项目(已下载的文件也会从本地删除)吗",
                    parent=self._window,
                    on_ok=lambda: self.delete_items(
                        cids,
                        checked,
                        False,
                        True
                    )
                )
            case "remove":
                self.delete_items(
                    cids,
                    checked,
                    False,
                    False
                )

    def delete_downloaded(self, item: DownloadedItem):
        self.handle_downloaded("delete")

    def remove_downloaded(self, item: DownloadedItem):
        self.handle_downloaded("remove")

    def pause_all(self):
        self.stop()

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
        for r in rows:
            row = dict(r)
            name = row["name"]
            cid = row["cid"]
            if row["status"] == 0:
                item = DownloadingItem(
                    name=name,
                    cid=cid,
                    aid=row["aid"],
                    quality=row["quality"],
                    album=row["album"],
                    vid=row["vid"],
                    size=row["size"] if "size" in row else 0
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
