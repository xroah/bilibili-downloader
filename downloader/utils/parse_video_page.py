import re
import json

from bs4 import BeautifulSoup

_info_prefix = "window.__playinfo__="
_state_prefix = "window.__INITIAL_STATE__="


def parse(html: str) -> dict:
    soup = BeautifulSoup(html, "html.parser")
    scripts = soup.select("script")

    for s in scripts:
        text = s.string

        if not text:
            continue

        text = re.sub(r"\s+", "", text.strip())

        if text.startswith(_info_prefix):
            text = text.replace(_info_prefix, "")
            info = json.loads(text)
            data = info["data"]
            quality = dict(zip(data["accept_description"], data["accept_quality"]))
        elif text.startswith(_state_prefix):
            text = text.replace(_state_prefix, "")
            # remove js code
            text = re.sub(r";.*;", "", text)
            state = json.loads(text)
            video_data = state["videoData"]
            title = video_data["title"]
            pages = video_data["pages"]
            bvid = video_data["bvid"]
            pic = video_data["pic"]

    ret = {
        "quality": quality,
        "title": title,
        "pages": pages,
        "bvid": bvid,
        "pic": pic
    }

    return ret
