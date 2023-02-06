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
        "msg": ""
    }
    try:
        res = get(f"{Req.REFERER}/video/{bvid}")
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
                if len(state.get("sections", [])):
                    sections = state["sections"]

                    for sec in sections[0]["episodes"]:
                        ret["episodes"].append({
                            "aid": sec["aid"],
                            "bvid": sec["bvid"],
                            "cid": sec["cid"],
                            "title": sec["title"]
                        })
                elif "videoData" in state:
                    video_data = state["videoData"]
                    pages = video_data["pages"]

                    for p in pages:
                        ret["episodes"].append({
                            "aid": video_data["aid"],
                            "bvid": video_data["bvid"],
                            "cid": p["cid"],
                            "title": p["part"]
                        })
                break

    return ret
