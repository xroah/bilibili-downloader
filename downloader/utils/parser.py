import re
import html
import json
from urllib.parse import urlparse
import os
from bs4 import BeautifulSoup

from .request import get
from ..enums import Req

_info_prefix = "window.__playinfo__="
_state_prefix = "window.__INITIAL_STATE__="


def parse_url(url: str):
    if not url.startswith("https://"):
        return url

    path = urlparse(url).path
    path = re.sub(r"/+$", "", path)

    return os.path.basename(path)



def is_error_page(text: str) -> bool:
    soup = BeautifulSoup(text, "html.parser")
    err_container = soup.select_one(".error-container")

    return err_container is not None


def get_video_page(bvid: str):
    ret = {
        "code": 0,
        "msg": "",
        "html_str": ""
    }
    try:
        res = get(f"{Req.VIDEO_PAGE}/{bvid}")
    except:
        ret["code"] = -1
        ret["msg"] = "请求发生错误"
    else:
        text = res.text

        if is_error_page(text):
            ret["code"] = -1
            ret["msg"] = "视频不存在"
        else:
            ret["html_str"] = text

    return ret


def get_episodes(html_str: str):
    ret = {
        "episodes": [],
        "album": "",
        "current": dict()
    }
    soup = BeautifulSoup(html_str, "html.parser")
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
            text = re.sub(r";[()]function.*", "", text)
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


def get_info(html_str: str):
    ret = {
        "code": -1,
        "title": ""
    }
    soup = BeautifulSoup(html_str, "html.parser")
    title = soup.select_one(".video-title")
    scripts = soup.select("script")

    if title is not None:
        ret["title"] = title.text

    for s in scripts:
        text = s.text.strip()

        if not text:
            continue

        if text.startswith(_info_prefix):
            ret["code"] = 0
            text = text.lstrip(_info_prefix)
            play_info = json.loads(text)
            dash = play_info["data"]["dash"]
            ret["duration"] = dash["duration"]
            ret["audio"] = dash["audio"]
            ret["video"] = dash["video"]

            break

    return ret
