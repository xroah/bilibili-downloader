import os
import time
from threading import Thread
from queue import Queue
from tqdm import tqdm
from peewee import JOIN

from .download_fille import download_file, merge
from ..db import Video, Season, Part
from ..enums import Status
from .get_info import get_video_url
from ..settings import settings


class Download:
    def __init__(self):
        self.items = []
        self.progress = None
        self.q = None
        self.t = None
        query = Part.select(
            Part.aid,
            Part.bvid,
            Part.title,
            Part.cid,
            Part.path,
            Part.multiple,
            Video,
            Season
        ).join(
            Video,
            JOIN.LEFT_OUTER,
            on=(Part.bvid == Video.bvid),
            attr="video"
        ).switch().join(
            Season,
            JOIN.LEFT_OUTER,
            on=(Part.season_id == Season.season_id),
            attr="season"
        ).where(Part.finished == False)

        for r in query:
            self.items.append(r)

        self.start_download()

    def new_progress(self):
        self.progress = tqdm(
            total=0,
            unit_scale=True,
            unit_divisor=1024,
            unit="B"
        )

    def start_download(self):
        if len(self.items) == 0:
            return

        item = self.items.pop(0)
        directory = "."

        if hasattr(item, "video"):
            directory = item.video.title
        elif hasattr(item, "season"):
            directory = item.season.title

        directory = os.path.join(settings.get("path"), directory)
        download_url = get_video_url(
            aid=item.aid,
            bvid=item.bvid,
            cid=item.cid
        )
        audio_name = os.path.join(
            directory,
            f"{item.cid}-audio.m4s"
        )
        video_name = os.path.join(
            directory,
            f"{item.cid}-video.m4s"
        )

        if not os.path.exists(directory):
            os.makedirs(directory)

        print(f"下载{item.title}音频")
        self.start_thread(download_url["audio_url"], audio_name)
        print(f"下载{item.title}视频")
        self.start_thread(download_url["video_url"], video_name)
        print("合成视频")
        merge(
            video_name,
            audio_name,
            os.path.join(directory, f"{item.title}.mp4")
        )

        self.start_download()

    def start_thread(self, url: str, filename: str) -> str:
        self.q = Queue()
        self.t = Thread(
            target=download_file,
            args=[
                url,
                filename,
                self.q
            ]
        )
        total = 0

        self.new_progress()
        self.t.start()

        while True:
            info = self.q.get()
            status = info["status"]
            size = int(info["size"])

            if status == str(Status.ERROR) or status == str(Status.DONE):
                break
            elif status == str(Status.START):
                total = size
                self.progress.reset(total=size)
            else:
                self.progress.update(size)

        self.t.join()

        if status == str(Status.DONE):
            self.progress.update(total)

        self.progress.close()
        time.sleep(.5)

        self.progress = None

        return status
