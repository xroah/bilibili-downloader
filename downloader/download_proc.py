import sys
from multiprocessing import Event, Queue
import os
from urllib.parse import urlparse
import subprocess
import time

from .settings import settings
from .enums import SettingsKey, Req, Status
from .utils import request, utils


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


def _download(
        *,
        album: str,
        url: str,
        event: Event,
        queue: Queue,
) -> bool | str:
    bytes_ = 0
    name = get_name(url)
    d_path = settings.get(SettingsKey.DOWNLOAD_PATH)
    album_dir = os.path.join(d_path, album)
    fullpath = os.path.join(d_path, album, name)

    if not os.path.exists(album_dir):
        os.makedirs(album_dir)

    if os.path.exists(fullpath):
        st = os.lstat(fullpath)
        bytes_ = st.st_size

    headers = {
        "range": f"bytes={bytes_}-"
    }
    err = {"status": Status.ERROR}

    try:
        res = request.get(url, headers=headers, stream=True)
    except Exception as e:
        print("Error", e)
        queue.put(err)
        return False
    else:
        start_time = time.time()
        if bytes_ > 0:
            queue.put({
                "status": Status.UPDATE,
                "chunk_size": bytes_
            })
        downloaded = 0
        with open(fullpath, "ab+") as f:
            for c in res.iter_content(chunk_size=1024 * 10):
                if c:
                    now = time.time()
                    interval = now - start_time
                    downloaded += len(c)
                    data = {
                        "status": Status.UPDATE,
                        "chunk_size": len(c),
                    }

                    if interval > 1:
                        speed = downloaded / interval
                        data["speed"] = speed
                        start_time = now
                        downloaded = 0

                    f.write(c)
                    queue.put(data)

                if event.is_set():
                    queue.put({
                        "status": Status.PAUSE
                    })
                    return False

    return fullpath


def get_video_url(videos: list[dict], quality: int):
    ret = ""

    for v in videos:
        q = v["id"]

        if q == quality or q < quality:
            ret = v["base_url"]
            break

    return ret


def merge(*, album, audio, video, name):
    d_path = settings.get(SettingsKey.DOWNLOAD_PATH)
    output = os.path.join(d_path, album, name) + ".mp4"
    ffmpeg = "ffmpeg.exe" if sys.platform == "win32" else "ffmpeg"
    subprocess.run([
        os.path.join(os.getcwd(), ffmpeg),
        "-i",
        audio,
        "-i",
        video,
        "-y",
        "-c",
        "copy",
        output
    ])
    try:
        os.unlink(audio)
        os.unlink(video)
    except:
        pass

    return output

def download(
        *,
        event: Event,
        queue: Queue,
        avid: int,
        bvid: str,
        cid: int,
        quality: int,
        name: str,
        album: str
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
            f"{Req.PLAY_URL}",
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

        if data["code"] != 0:
            queue.put(err)
            return

        data = data["data"]
        dash = data["dash"]
        audio_url = dash["audio"][0]["base_url"]
        video_url = get_video_url(dash["video"], quality)
        audio_size = get_size(audio_url)
        video_size = get_size(video_url)

        if video_size == -1 or audio_size == -1:
            queue.put(err)
            return
        queue.put({
            "status": Status.UPDATE,
            "total": video_size + audio_size
        })
        audio = _download(
            album=album,
            url=audio_url,
            event=event,
            queue=queue
        )

        if not audio:
            return

        video = _download(
            album=album,
            url=video_url,
            event=event,
            queue=queue
        )

        if not video:
            return

        queue.put({"status": Status.MERGE})
        video_path = merge(
            album=album,
            audio=audio,
            video=video,
            name=name
        )
        queue.put({
            "status": Status.DONE,
            "video_path": os.path.normpath(video_path)
        })
