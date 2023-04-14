import subprocess
from queue import Queue
import os

from ..utils.request import get
from ..enums import Status
from ..utils.utils import print_error


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
    total = res.headers["Content-Length"]
    ret = {
        "status": "start",
        "size": total,
    }
    err_msg = "下载出错"

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
        print_error(err_msg)
    else:
        stat = os.lstat(filename)
        if stat.st_size != range_start + total:
            ret["status"] = str(Status.ERROR)
            print_error(err_msg)
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
