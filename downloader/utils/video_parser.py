import re
import os.path
from urllib.parse import urlparse
import html
import json
from bs4 import BeautifulSoup

from .request import get
from ..enums import Req

_info_prefix = "window.__playinfo__="
_state_prefix = "window.__INITIAL_STATE__="


def match_video_id(vid: str) -> bool:
    av_pattern = r"^av\d+$"
    bv_pattern = r"^bv[\da-zA-Z]{10}$"

    if (
            re.fullmatch(av_pattern, vid, re.IGNORECASE) or
            re.fullmatch(bv_pattern, vid, re.IGNORECASE)
    ):
        return True

    return False


def parse_url(url: str) -> str | None:
    if not url.strip():
        return

    matched = match_video_id(url)

    if matched:
        return url

    if "bilibili.com" not in url:
        return None

    # like: https://www.bilibili.com/video/BVxxxx/?xxx
    path = urlparse(url).path.rstrip("/")
    base = os.path.basename(path)
    matched = match_video_id(base)

    if matched:
        return base

    return None


def get_episodes(bvid: str):
    ret = {
        "episodes": [],
        "code": 0,
        "msg": "",
        "album": "",
        "current": dict()
    }
    try:
        res = get(f"{Req.VIDEO_PAGE}/{bvid}")
    except:
        ret["code"] = -1
        ret["msg"] = "请求发生错误"
    else:
        soup = BeautifulSoup(res.text, "html.parser")
        scripts = soup.select("script")

        for s in scripts:
            text = s.string

            if not text:
                continue

            text = re.sub(r"\s+", "", text.strip())
            text = html.unescape(text)

            if text.startswith(_state_prefix):
                text = text.replace(_state_prefix, "")
                # remove js code
                text = re.sub(r";[\(\)]function.*", "", text)
                state = json.loads(text)
                video_data = state["videoData"]
                c = ret["current"]
                c["aid"] = video_data["aid"]
                c["bvid"] = video_data["bvid"]
                c["cid"] = video_data["cid"]
                c["title"] = video_data["title"]

                if len(state.get("sections", [])):
                    sections = state["sections"]
                    ret["album"] = state["sectionsInfo"]["title"]

                    for sec in sections[0]["episodes"]:
                        ret["episodes"].append({
                            "aid": sec["aid"],
                            "bvid": sec["bvid"],
                            "cid": sec["cid"],
                            "title": sec["title"]
                        })
                else:
                    pages = video_data["pages"]
                    ret["album"] = video_data["title"]

                    for p in pages:
                        episode = c.copy()
                        episode["title"] = p["part"]
                        ret["episodes"].append(episode)
                break

    return ret


def get_info(bvid: str):
    ret = {
        "code": 0,
        "msg": "",
        "info": dict()
    }

    try:
        res = get(f"{Req.VIDEO_PAGE}/{bvid}")
    except:
        ret["code"] = -1
        ret["msg"] = "获取视频信息失败"
    else:
        soup = BeautifulSoup(res.text, "html.parser")
        info = ret["info"]
        title = html.unescape(soup.select_one(".video-title").text)
        info["title"] = title
        scripts = soup.select("script")

        for s in scripts:
            text = s.text.strip()

            if not s:
                continue

            if text.startswith(_info_prefix):
                text = text.lstrip(_info_prefix)
                play_info = json.loads(text)
                dash = play_info["data"]["dash"]
                info["duration"] = dash["duration"]
                info["audio"] = dash["audio"]
                info["video"] = dash["video"]

                break

    return ret
