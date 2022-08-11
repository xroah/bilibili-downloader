import re
import json
import html

from bs4 import BeautifulSoup

_info_prefix = "window.__playinfo__="
_state_prefix = "window.__INITIAL_STATE__="


def parse(html_text: str) -> dict:
    soup = BeautifulSoup(html_text, "html.parser")
    qualities = {}
    title = ""
    bvid = ""
    pic = ""
    avid = ""
    pages = []
    scripts = soup.select("script")

    for s in scripts:
        text = s.string

        if not text:
            continue

        text = re.sub(r"\s+", "", text.strip())
        text = html.unescape(text)

        if text.startswith(_info_prefix):
            text = text.replace(_info_prefix, "")
            info = json.loads(text)
            data = info["data"]
            qualities = dict(zip(data["accept_description"], data["accept_quality"]))
        elif text.startswith(_state_prefix):
            text = text.replace(_state_prefix, "")
            # remove js code
            text = re.sub(r";[\(\)]function.*", "", text)
            state = json.loads(text)
            if "videoData" not in state:
                continue
            video_data = state["videoData"]
            if "bvid" not in video_data:
                continue
            title = re.sub(r"[:*<>?\"'|]", " ", video_data["title"])
            pages = video_data["pages"]
            bvid = video_data["bvid"]
            pic = video_data["pic"]
            avid = video_data["aid"]

    ret = {
        "qualities": qualities,
        "title": title,
        "pages": pages,
        "bvid": bvid,
        "pic": pic,
        "avid": avid
    }

    return ret
