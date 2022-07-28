import re
import json
import html

from bs4 import BeautifulSoup

_info_prefix = "window.__playinfo__="
_state_prefix = "window.__INITIAL_STATE__="


def parse(html_text: str) -> dict:
    soup = BeautifulSoup(html_text, "html.parser")
    quality = {}
    title = ""
    bvid = ""
    pic = ""
    pages = []
    scripts = soup.select("script")
    has_info = False
    has_state = False

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
            quality = dict(zip(data["accept_description"], data["accept_quality"]))
            has_info = True
        elif text.startswith(_state_prefix):
            text = text.replace(_state_prefix, "")
            # remove js code
            text = re.sub(r";[\()]function.*", "", text)
            state = json.loads(text)
            video_data = state["videoData"]
            title = video_data["title"]
            pages = video_data["pages"]
            bvid = video_data["bvid"]
            pic = video_data["pic"]
            has_state = True

    ret = {
        "quality": quality,
        "title": title,
        "pages": pages,
        "bvid": bvid,
        "pic": pic,
        "has_info": has_info,
        "has_state": has_state
    }

    return ret
