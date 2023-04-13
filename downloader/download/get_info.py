from urllib.parse import urlencode
import time

from ..utils import request
from ..enums import Req
from ..utils.encrypt_params import encrypt
from ..db import Part, Video, Season
from ..settings import settings
from ..db.BaseModel import date_format

# reference: https://github.com/SocialSisterYi/bilibili-API-collect/blob/master/docs/video/videostream_url.md
"""
video qualities:
6	240P 极速
16	360P 流畅
32	480P 清晰
64	720P 高清
74	720P60 高帧率
80	1080P 高清
112	1080P+ 高码率
116	1080P60 高帧率
120	4K 超清
125	HDR 真彩色
126	杜比视界
127	8K 超高清
"""
"""
audio qualities:
30216	64K
30232	132K
30280	192K
30250	杜比全景声
30251	Hi-Res无损
"""


def save_to_db(obj: dict):
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


def get_videos_by_bvid(bvid: str, one=False) -> dict:
    ret = {
        "code": 0,
        "video_data": {
            "is_season": False,
            "season_id": "",
            "videos": [],
            "title": ""
        }
    }
    params = encrypt(f"bvid={bvid}")
    json = request.get_json(str(Req.VIEW_URL) + "?" + params)

    if json["code"] != 0:
        return json

    data = json["data"]
    videos = ret["video_data"]["videos"]

    if "ugc_season" in data:
        season = data["ugc_season"]
        section = season["sections"][0]
        ret["video_data"]["is_season"] = True
        ret["video_data"]["title"] = season["title"]
        season_id = section["season_id"]
        ret["video_data"]["season_id"] = season_id
        episodes = section["episodes"]
        videos.append({
            "aid": data["aid"],
            "bvid": data["bvid"],
            "cid": data["cid"],
            "title": data["title"],
            "page": 1,
            "season_id": season_id
        })

        if not one:
            for e in episodes:
                if e["bvid"] != data["bvid"]:
                    videos.append({
                        "aid": e["aid"],
                        "bvid": e["bvid"],
                        "cid": e["cid"],
                        "page": 1,
                        "title": e["title"],
                        "season_id": season_id
                    })
    elif "pages" in data:
        pages = data["pages"]
        ret["video_data"]["title"] = data["title"]

        for p in pages:
            videos.append({
                "aid": data["aid"],
                "bvid": data["bvid"],
                "cid": p["cid"],
                "page": p["page"],
                "title": p["part"]
            })

    save_to_db(ret)

    return ret


def get_video_url(
        aid: int,
        bvid: str,
        cid: int,
        qn: int = 80
) -> dict:
    ret = {
        "code": 0,
        "audio_url": "",
        "video_url": "",
        "quality": qn
    }
    params = {
        "avid": aid,
        "bvid": bvid,
        "cid": cid,
        "fnval": 16,
        "fnver": 0,
        "fourk": 1,
        "gaia_source": "",
        "qn": 0
    }
    params = encrypt(urlencode(params))
    json = request.get_json(str(Req.PLAY_URL) + "?" + params)

    if json["code"] != 0:
        return json

    default_audio = 30232
    data = json["data"]
    dash = data["dash"]
    audios = dash["audio"]
    videos = dash["video"]

    for a in audios:
        if a["id"] == default_audio:
            ret["audio_url"] = a["base_url"]

    if ret["audio_url"] == "":
        ret["audio_url"] = audios[0]["base_url"]

    for v in videos:
        if v["id"] == qn:
            ret["video_url"] = v["base_url"]

    if ret["video_url"] == "":
        videos.sort(key=lambda video: video["id"], reverse=True)
        ret["video_url"] = videos[0]["base_url"]
        ret["quality"] = videos[0]["id"]

    return ret
