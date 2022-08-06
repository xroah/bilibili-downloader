from multiprocessing import Event, Queue
import os
from pickle import FALSE
from urllib.parse import urlparse
import subprocess

from .settings import settings
from .enums import SettingsKey, Req, Status
from .utils import utils, request


def get_size(url):
    try:
        res = request.head(url)
    except:
        return -1
    else:
        if res.status_code != 200:
            return -1

        return float(res.headers["content-length"])


def get_name(url):
    parsed = urlparse(url)
    name = os.path.basename(parsed.path)

    return name


def _download(url: str, evt: Event, q: Queue) -> bool | str:
    bytes = 0
    name = get_name(url)
    d_path = settings.get(SettingsKey.DOWNLOAD_PATH)
    fullpath = os.path.join(d_path, name)

    if os.path.exists(fullpath):
        st = os.lstat(fullpath)
        bytes = st.st_size

    headers = {
        "range": f"bytes={bytes}-"
    }
    err = {"status": Status.ERROR}

    try:
        res = request.get(url, headers=headers, stream=True)
    except Exception as e:
        print("Error", e)
        q.put(err)
        return False
    else:
        code = res.status_code
        if code >= 300:
            q.put(err)
            return False

        with open(fullpath, "ab+") as f:
            for c in res.iter_content(chunk_size=1024*10):
                if c:
                    f.write(c)
                    q.put({
                        "status": Status.UPDATE,
                        "data": len(c)
                    })

                if evt.is_set():
                    q.put({
                        "status": Status.PAUSE
                    })
                    return FALSE

    return fullpath


def get_video_url(videos: list[dict], quality: int):
    ret = ""

    for v in videos:
        q = v["id"]

        if q == quality or q < quality:
            ret = v["base_url"]
            break

    return ret


def merge(audio, video, name):
    subprocess.run([
        "ffmpeg",
        "-i",
        audio,
        "-i",
        video,
        "-y",
        "-c",
        "copy",
        f"{name}.mp4"
    ])


def download(
    *
    event: Event,
    queue: Queue,
    avid: int,
    bvid: str,
    cid: int,
    quality: int,
    name: str
):
    params = {
        "avid": avid,
        "bvid": bvid,
        "cid": cid,
        "qn": 0,
        "fnver": 0,
        "fnval": 4048,
        "fourk": 1,
    }
    err = {
        "status": Status.ERROR
    }
    try:
        res = request.get(
            f"{Req.API_ADDR}{Req.URL_PATH}",
            params=params
        )
        code = res.status_code
    except:
        queue.put(err)
    else:
        if code != 200:
            queue.put(err)
            return

        data = res.json()

        if data.code != 0:
            queue.put(err)
            return

        data = data["data"]
        dash = data["dash"]
        audio_url = dash["audio"][0]["base_url"]
        video_url = get_video_url(dash["video"], quality)
        audio = _download(audio_url, event, queue)

        if not audio:
            return

        video = _download(video_url, event, queue)

        if not video:
            return

        merge(audio, video, name)
        queue.put({"status": Status.DONE})
