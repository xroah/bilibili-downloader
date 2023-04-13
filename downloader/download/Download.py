from threading import Thread
from queue import Queue
import time

from .get_info import get_videos_by_bvid
from ..db import Part, Video, Season
from ..settings import settings
from ..db.BaseModel import date_format


class Download:
    def __init__(self, obj: dict):
        if obj["code"] != 0:
            return

        video_data = obj["video_data"]
        is_season = video_data["is_season"]
        videos = video_data["videos"]
        data = []
        multiple = len(videos) > 1 or is_season

        for v in videos:
            v["create_time"] = time.strftime(date_format)
            v["finished"] = False
            v["multiple"] = multiple
            v["path"] = settings.get("path")

            data.append(v)

        if multiple:
            if not is_season:
                v = videos[0]

                Video.insert({
                    "bvid": v["bvid"],
                    "title": video_data["title"],
                    "create_time": time.strftime(date_format)
                }) \
                    .on_conflict_ignore(True) \
                    .execute()
            else:
                Season.insert({
                    "season_id": video_data["season_id"],
                    "title": video_data["title"],
                    "create_time": time.strftime(date_format)
                }) \
                    .on_conflict_ignore(True) \
                    .execute()

        Part \
            .insert_many(data) \
            .on_conflict_ignore(True) \
            .execute()
