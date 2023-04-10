from urllib.parse import urlencode

from ..utils import request
from ..enums import Req
from ..utils.encrypt_params import encrypt

# qn reference: https://github.com/SocialSisterYi/bilibili-API-collect/blob/master/docs/video/videostream_url.md#qn%E8%A7%86%E9%A2%91%E6%B8%85%E6%99%B0%E5%BA%A6%E6%A0%87%E8%AF%86
"""
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
# audio reference: https://github.com/SocialSisterYi/bilibili-API-collect/blob/master/docs/video/videostream_url.md#%E8%A7%86%E9%A2%91%E4%BC%B4%E9%9F%B3%E9%9F%B3%E8%B4%A8%E4%BB%A3%E7%A0%81
"""
30216	64K
30232	132K
30280	192K
30250	杜比全景声
30251	Hi-Res无损
"""


def get_videos_by_bvid(bvid: str, one=False) -> dict:
    ret = {
        "code": 0,
        "title": "",
        "video_data": {
            "is_season": False,
            "videos": []
        }
    }
    params = encrypt(f"bvid={bvid}")
    json = request.get_json(str(Req.VIEW_URL) + "?" + params)

    if json["code"] != 0:
        return json

    data = json["data"]
    videos = ret["video_data"]["videos"]

    if "ugc_season" in data:
        section = data["ugc_season"]["sections"][0]
        ret["video_data"]["is_season"] = True
        ret["title"] = section["title"]
        ret["video_data"]["season_id"] = section["season_id"]
        episodes = section["episodes"]
        videos.append({
            "aid": data["aid"],
            "bvid": data["bvid"],
            "cid": data["cid"],
            "title": data["title"],
        })

        if not one:
            for e in episodes:
                if e["bvid"] != data["bvid"]:
                    videos.append({
                        "aid": e["aid"],
                        "bvid": e["bvid"],
                        "cid": e["cid"],
                        "title": e["title"]
                    })
    elif "pages" in data:
        pages = data["pages"]
        for p in pages:
            if p["cid"] != data["cid"]:
                videos.append({
                    "aid": data["aid"],
                    "bvid": data["bvid"],
                    "page": p["page"],
                    "title": p["part"]
                })

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
        videos.sort(key=lambda v: v["id"], reverse=True)
        ret["video_url"] = videos[0]["base_url"]

    return ret
