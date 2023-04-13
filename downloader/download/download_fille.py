import subprocess
import time
from queue import Queue
import os

from ..utils.request import get
from ..enums import Status


def download_file(url: str, filename: str, q: Queue):
    exists = os.path.exists(filename)
    range_start = 0

    if exists:
        stat = os.lstat(filename)
        range_start = stat.st_size

    res = get(
        url,
        stream=True,
        headers={
            "range": f"bytes={range_start}-"
        }
    )
    ret = {
        "status": "start",
        "size": res.headers["Content-Length"],
    }

    q.put(ret)

    try:
        with open(filename, "ab+") as f:
            for chunk in res.iter_content(chunk_size=10 * 1024):
                ret["status"] = str(Status.UPDATE)
                ret["size"] = len(chunk)

                q.put(ret)
                f.write(chunk)
    except:
        ret["status"] = str(Status.ERROR)
    else:
        ret["status"] = str(Status.DONE)

    q.put(ret)


def merge(audio: str, video: str, output: str):
    subprocess.run([
        "ffmpeg",
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
