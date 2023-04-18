import os
import re
import sys
import time
from threading import Thread
from queue import Queue
from tqdm import tqdm
from peewee import JOIN
from typing import cast

from .download_fille import download_file, merge
from ..db import Video, Season, Part, Episode
from ..db.BaseModel import date_format
from ..enums import Status
from .get_info import get_video_url, get_episode_url
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
        e_query = Episode.select(
            Episode.aid,
            Episode.ep_id,
            Episode.cid,
            Episode.title,
            Season
        ).join(
            Season,
            JOIN.LEFT_OUTER,
            on=(Episode.season_id == Season.season_id),
            attr="season"
        ).where(Episode.finished == False)

        for r in query:
            self.items.append(r)

        for r in e_query:
            self.items.append(r)

        self.start_download()

    def new_progress(self):
        self.progress = tqdm(
            total=0,
            unit_scale=True,
            unit_divisor=1024,
            unit="B"
        )

    @staticmethod
    def update_db(item: Part | Episode, output: str, qn: int):
        # downloaded and merged successfully
        if not os.path.exists(output):
            return

        finish_time = time.strftime(date_format)

        if hasattr(item, "ep_id"):
            item = cast(Episode, item)
            q = Episode.update({
                Episode.finished: True,
                Episode.finish_time: finish_time,
                Episode.quality: qn,
                Episode.path: output
            }).where(
                (Episode.ep_id == item.ep_id) &
                (Episode.aid == item.aid)
            )
        else:
            q = Part.update({
                Part.finished: True,
                Part.finish_time: finish_time,
                Part.quality: qn,
                Part.path: output
            }).where(
                (Part.bvid == item.bvid) &
                (Part.cid == item.cid)
            )

        q.execute()

    @staticmethod
    def handle_path(*args):
        p = os.path.join(*args)

        return os.path.normpath(p)

    def get_name(self, item: Part | Episode):
        directory = "."
        if hasattr(item, "video"):
            directory = item.video.title  # type: ignore
        elif hasattr(item, "season"):
            directory = item.season.title  # type: ignore

        pattern = r'[/\\":*<>|?]'
        name = re.sub(pattern, "", cast(str, item.title))
        directory = re.sub(pattern, "", directory)
        directory = self.handle_path(settings.get("path"), directory)
        audio_name = self.handle_path(directory, f"{item.cid}_a")
        video_name = self.handle_path(directory, f"{item.cid}_v")
        output = self.handle_path(directory, f"{name}.mp4")

        if not os.path.exists(directory):
            os.makedirs(directory)

        return audio_name, video_name, output

    @staticmethod
    def get_download_url(item: Part | Episode):
        aid = cast(int, item.aid)
        cid = cast(int, item.cid)

        if hasattr(item, "ep_id"):
            item = cast(Episode, item)

            return get_episode_url(
                aid=aid,
                ep_id=cast(int, item.ep_id),
                cid=cid
            )

        item = cast(Part, item)

        return get_video_url(
            aid=aid,
            cid=cid,
            bvid=cast(str, item.bvid)
        )

    def start_download(self):
        if len(self.items) == 0:
            print("=" * 20 + "完成" + "=" * 20)
            return

        item = self.items.pop(0)
        d_url = self.get_download_url(item)

        if not d_url:
            return self.start_download()

        (audio_name, video_name, output) = self.get_name(item)
        ext = ".m4s"
        tmp_ext = ".tmp"
        audio_tmp = audio_name + tmp_ext
        video_tmp = video_name + tmp_ext
        audio_m4s = audio_name + ext
        video_m4s = video_name + ext

        try:
            # already downloaded
            if not os.path.exists(audio_m4s):
                print(f"正在下载'{item.title}'音频")
                a_success = self.start_thread(
                    d_url["audio_url"],
                    audio_tmp
                )

                if a_success:
                    os.rename(audio_tmp, audio_m4s)
            else:
                a_success = True

            if not os.path.exists(video_m4s):
                print(f"正在下载'{item.title}'视频")
                v_success = self.start_thread(
                    d_url["video_url"],
                    video_tmp
                )

                if v_success:
                    os.rename(video_tmp, video_m4s)
            else:
                v_success = True

            if a_success and v_success:
                print("正在合成视频...")
                merge(audio_m4s, video_m4s, output)
        except KeyboardInterrupt:
            sys.exit(1)
        except Exception as E:
            raise E

        self.update_db(item, output, d_url["quality"])
        self.start_download()

    def start_thread(self, url: str, filename: str) -> bool:
        self.q = Queue()
        self.t = Thread(
            target=download_file,
            args=[
                url,
                filename,
                self.q
            ]
        )
        self.t.daemon = True

        self.new_progress()
        self.t.start()

        progress = cast(tqdm, self.progress)

        while True:
            info = self.q.get()
            status = info["status"]
            size = int(info["size"])

            if status == str(Status.ERROR) or status == str(Status.DONE):
                break
            elif status == str(Status.START):
                progress.reset(total=size)
            else:
                progress.update(size)

        self.t.join()
        progress.close()
        time.sleep(.5)

        self.progress = None
        self.q = None
        self.t = None

        return status == str(Status.DONE)
