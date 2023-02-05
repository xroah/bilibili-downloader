import re
import os.path
from urllib.parse import urlparse
from .request import get
from ..enums import Req


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


def get_html(url: str):
    vid = parse_url(url)

    if vid:
        res = get(f"{Req.REFERER}/video/{vid}")

        return res.text
    else:
        return None
