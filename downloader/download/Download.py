from threading import Thread
from queue import Queue
import time

from .get_info import get_videos_by_bvid
from ..db.VideoTable import Video, date_format


class Download:
    def __init__(self, obj: dict):
        if obj["code"] != 0:
            return

        video_data = obj["video_data"]
        is_season = video_data["is_season"]
        videos = video_data["videos"]
        data = []
        multiple = len(videos) > 1

        for v in videos:
            v["create_time"] = time.strftime(date_format)
            v["finished"] = False
            v["multiple"] = multiple

            data.append(v)

        Video.insert_many(data).on_conflict_ignore(True).execute()
