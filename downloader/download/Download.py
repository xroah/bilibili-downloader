import os
import re
import sys
import time
from threading import Thread
from queue import Queue
from tqdm import tqdm
from peewee import JOIN

from .download_fille import download_file, merge
from ..db import Video, Season, Part
from ..db.BaseModel import date_format
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

        download_info = get_video_url(
            aid=item.aid,
            bvid=item.bvid,
            cid=item.cid
        )
        pattern = r'[/\\":*<>|?]'
        name = re.sub(pattern, "", item.title)
        directory = re.sub(pattern, "", directory)
        directory = os.path.join(settings.get("path"), directory)
        audio_name = os.path.join(
            directory,
            f"{item.cid}_a"
        )
        video_name = os.path.join(
            directory,
            f"{item.cid}_v"
        )
        ext = ".m4s"
        tmp_ext = ".tmp"
        audio_tmp = audio_name + tmp_ext
        video_tmp = video_name + tmp_ext
        audio_m4s = audio_name + ext
        video_m4s = video_name + ext
        output = os.path.join(directory, f"{name}.mp4")

        if not os.path.exists(directory):
            os.makedirs(directory)

        try:
            if not os.path.exists(audio_m4s):
                print(f"正在下载'{item.title}'音频")
                self.start_thread(download_info["audio_url"], audio_tmp)
                os.rename(audio_tmp, audio_m4s)

            if not os.path.exists(video_m4s):
                print(f"正在下载'{item.title}'视频")
                self.start_thread(download_info["video_url"], video_tmp)
                os.rename(video_tmp, video_m4s)

            print("正在合成视频...")
            merge(audio_m4s, video_m4s, output)
        except KeyboardInterrupt:
            sys.exit(1)
        except Exception as E:
            raise E

        # downloaded and merged successfully
        if os.path.exists(output):
            Part.update({
                Part.finished: True,
                Part.finish_time: time.strftime(date_format),
                Part.quality: download_info["quality"],
                Part.path: output
            }).where((Part.bvid == item.bvid) & (Part.cid == item.cid)) \
                .execute()

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
        self.t.daemon = True

        self.new_progress()
        self.t.start()

        while True:
            info = self.q.get()
            status = info["status"]
            size = int(info["size"])

            if status == str(Status.ERROR) or status == str(Status.DONE):
                break
            elif status == str(Status.START):
                self.progress.reset(total=size)
            else:
                self.progress.update(size)

        self.t.join()
        self.progress.close()
        time.sleep(.5)

        self.progress = None
        self.q = None
        self.t = None

        return status
