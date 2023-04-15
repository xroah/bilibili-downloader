from urllib.parse import urlencode
import time
import re

from ..utils import request
from ..enums import Req
from ..utils.encrypt_params import encrypt
from ..db import Part, Video, Season, Episode
from ..utils.utils import print_warning, print_error
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


def save_videos_to_db(obj: dict):
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


def get(b_id: str, *args):
    v_pattern = r"^av|^bv"
    e_pattern = r"^ss|^ep"
    is_video = re.match(v_pattern, b_id, flags=re.IGNORECASE)
    is_episode = re.match(e_pattern, b_id, flags=re.IGNORECASE)

    if is_video is None and is_episode is None:
        print_error("id不正确")
        return

    if is_video is not None:
        get_videos(b_id, *args)
        return

    get_episodes(b_id)


def get_videos(bvid: str, one=False) -> dict:
    ret = {
        "code": 0,
        "video_data": {
            "is_season": False,
            "season_id": "",
            "videos": [],
            "title": ""
        }
    }
    is_av_id = re.match(
        r"^av",
        bvid,
        flags=re.IGNORECASE
    ) is not None
    params = encrypt(f"aid={bvid[2:]}" if is_av_id else f"bvid={bvid}")
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

        if len(pages) == 1:
            videos.append({
                "aid": data["aid"],
                "bvid": data["bvid"],
                "cid": data["cid"],
                "page": 1,
                "title": data["title"]
            })
        else:
            for p in pages:
                videos.append({
                    "aid": data["aid"],
                    "bvid": data["bvid"],
                    "cid": p["cid"],
                    "page": p["page"],
                    "title": p["part"]
                })

    save_videos_to_db(ret)

    return ret


def save_episodes_to_db(obj: dict):
    if obj["code"] != 0:
        return

    data = obj["ep_data"]
    episodes = data["episodes"]
    create_time = time.strftime(date_format)

    if len(episodes) > 1:
        Season.insert({
            "title": data["title"],
            "season_id": data["season_id"],
            "create_time": create_time
        }) \
            .on_conflict_ignore(True) \
            .execute()

    eps = []

    for e in episodes:
        item = e.copy()
        item["finished"] = False
        item["create_time"] = create_time

        eps.append(item)

    Episode \
        .insert_many(eps) \
        .on_conflict_ignore(True) \
        .execute()


def get_episodes(ep_id: str):
    is_season_id = re.match(
        r"^ss",
        ep_id,
        flags=re.IGNORECASE
    ) is not None
    id_ = ep_id[2:]
    params = f"season_id={id_}" if is_season_id else f"ep_id={id_}"
    json = request.get_json(str(Req.SEASON_URL) + "?" + params)
    ret = {
        "code": 0,
        "ep_data": {
            "title": "",
            "episodes": [],
            "season_id": ""
        }
    }

    if json["code"] != 0:
        return json

    data = json["result"]
    eps = data["episodes"]
    episodes = ret["ep_data"]["episodes"]
    season_id = data["season_id"]
    ret["ep_data"]["season_id"] = season_id
    season_title = data["season_title"]
    ret["ep_data"]["title"] = season_title
    multiple = len(eps) > 1

    for e in eps:
        title = e["share_copy"]

        if multiple:
            title = title\
                .replace(season_title, "")\
                .replace("《", "")\
                .replace("》", "")

        episodes.append({
            "title": title,
            "ep_id": e["id"],
            "aid": e["aid"],
            "cid": e["cid"],
            "bvid": e["bvid"],
            "season_id": season_id
        })

    save_episodes_to_db(ret)

    return ret


def get_info_from_dash(dash: dict, qn: int):
    default_audio = 30232
    ret = {
        "audio_url": "",
        "video_url": "",
        "quality": qn
    }

    audios = dash["audio"]
    videos = dash["video"]

    for a in audios:
        if a["id"] == default_audio:
            ret["audio_url"] = a["base_url"]

    if ret["audio_url"] == "":
        ret["audio_url"] = audios[0]["base_url"]

    for v in videos:
        if v["id"] == qn and "avc" in v["codecs"]:
            ret["video_url"] = v["base_url"]

    if ret["video_url"] == "":
        videos.sort(key=lambda video: video["id"], reverse=True)

        for v in videos:
            if "avc" in v["codecs"]:
                ret["video_url"] = videos[0]["base_url"]
                ret["quality"] = videos[0]["id"]
                break

    return ret


def get_url(url: str, params: dict, qn: int) -> dict | None:
    params = encrypt(urlencode(params))
    json = request.get_json(url + "?" + params)

    if json["code"] != 0:
        return None

    data = json["data"] if "data" in json else json["result"]

    if "dash" not in data:
        print_warning("没有获取到下载地址，可能需要登录或者开通会员")
        return None

    return get_info_from_dash(data["dash"], qn)


def get_video_url(
        aid: int,
        bvid: str,
        cid: int,
        qn: int = 80
) -> dict | None:
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

    return get_url(str(Req.PLAY_URL), params, qn)


def get_episode_url(
        aid: int,
        ep_id: int,
        cid: int,
        qn: int = 80
) -> dict | None:
    params = {
        "support_multi_audio": True,
        "avid": aid,
        "cid": cid,
        "qn": 0,
        "fnver": 0,
        "fnval": 16,
        "fourk": 1,
        "ep_id": ep_id,
        "from_client": "BROWSER",
        "drm_tech_type": 2
    }

    return get_url(str(Req.EP_PLAY_URL), params, qn)
