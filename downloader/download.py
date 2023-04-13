# import sys
# from multiprocessing import Queue
# from threading import Event
# import os
# import subprocess
# import time
#
# from .db import DB
# from .settings import settings
# from .enums import SettingsKey, Req, Status
# from .utils import request
#
#
# def get_album_dir(album: str) -> str:
#     d_path = settings.get(SettingsKey.DOWNLOAD_PATH)
#     album_dir = os.path.normpath(os.path.join(d_path, album))
#
#     if not os.path.exists(album_dir):
#         os.makedirs(album_dir)
#
#     return album_dir
#
#
# def get_size(url):
#     try:
#         res = request.get(url, stream=True)
#     except:
#         return -1
#     else:
#         if res.status_code != 200:
#             return -1
#
#         return float(res.headers["content-length"])
#
#
# def get_fullpath(cid: int, type_: str, album: str) -> str:
#     name = f"{cid}-{type_}.tmp"
#     fullpath = os.path.join(get_album_dir(album), name)
#
#     return os.path.normpath(fullpath)
#
#
# def get_video_url(videos: list[dict], quality: int):
#     ret = ""
#
#     for v in videos:
#         q = v["id"]
#
#         if q == quality or q < quality:
#             ret = v["base_url"]
#             break
#
#     return ret
#
#
# def download_media(
#         *,
#         album: str,
#         url: str,
#         event: Event,
#         queue: Queue,
#         size: float,
#         type_: str,
#         cid: int
# ) -> bool | str:
#     bytes_ = 0
#     fullpath = get_fullpath(cid, type_, album)
#
#     if os.path.exists(fullpath):
#         st = os.lstat(fullpath)
#         bytes_ = st.st_size
#
#     if bytes_ == size:
#         return fullpath
#
#     headers = {
#         "range": f"bytes={bytes_}-"
#     }
#     err = {"status": Status.ERROR}
#
#     try:
#         res = request.get(url, headers=headers, stream=True)
#     except Exception as e:
#         print("Error", e)
#         queue.put(err)
#         return False
#     else:
#         code = res.status_code
#
#         if code > 300:
#             queue.put(err)
#             return False
#
#         start_time = time.time()
#         downloaded = 0
#         speed = 0
#         with open(fullpath, "ab+") as f:
#             for c in res.iter_content(chunk_size=1024 * 10):
#                 if c:
#                     now = time.time()
#                     interval = now - start_time
#                     downloaded += len(c)
#                     data = {
#                         "status": Status.UPDATE,
#                         "chunk_size": len(c),
#                     }
#
#                     if interval > 1:
#                         speed = downloaded / interval
#                         data["speed"] = speed
#                         start_time = now
#                         downloaded = 0
#                     elif interval > 0 and not speed:
#                         speed = len(c) / interval
#                         data["speed"] = speed
#
#                     f.write(c)
#                     queue.put(data)
#
#                 if event.is_set():
#                     queue.put({
#                         "status": Status.PAUSE
#                     })
#                     return False
#
#     return fullpath
#
#
# def merge(*, album, audio, video, name):
#     d_path = settings.get(SettingsKey.DOWNLOAD_PATH)
#     output = os.path.join(d_path, album, name) + ".mp4"
#     subprocess.run((
#         "ffmpeg",
#         "-i",
#         audio,
#         "-i",
#         video,
#         "-y",
#         "-c",
#         "copy",
#         output
#     ))
#     try:
#         os.unlink(audio)
#         os.unlink(video)
#     except:
#         pass
#
#     return output
#
#
# def download(
#         *,
#         event: Event,
#         queue: Queue,
#         avid: int,
#         bvid: str,
#         cid: int,
#         quality: int,
#         name: str,
#         album: str,
#         has_size=False
# ):
#     params = {
#         "avid": avid,
#         "bvid": bvid,
#         "cid": cid,
#         "qn": 0,
#         "fnver": 0,
#         "fnval": 4048,
#         "fourk": 1,
#     }
#     err = {
#         "status": Status.ERROR
#     }
#
#     try:
#         res = request.get(
#             f"{Req.PLAY_URL}",
#             params=params
#         )
#     except:
#         queue.put(err)
#     else:
#         code = res.status_code
#
#         if code != 200:
#             queue.put(err)
#             print("Status code is not 200: ", res.text)
#             return
#
#         data = res.json()
#
#         if data["code"] != 0:
#             queue.put(err)
#             return
#
#         data = data["data"]
#         dash = data["dash"]
#         audio_url = dash["audio"][0]["base_url"]
#         video_url = get_video_url(dash["video"], quality)
#         audio_size = get_size(audio_url)
#         video_size = get_size(video_url)
#
#         if video_size == -1 or audio_size == -1:
#             queue.put(err)
#             return
#
#         if not has_size:
#             queue.put({
#                 "status": Status.UPDATE,
#                 "total": video_size + audio_size
#             })
#
#             with DB() as db:
#                 db.update_size(cid, video_size + audio_size)
#
#         audio = download_media(
#             album=album,
#             url=audio_url,
#             event=event,
#             queue=queue,
#             size=audio_size,
#             type_="audio",
#             cid=cid
#         )
#
#         if not audio:
#             return
#
#         video = download_media(
#             album=album,
#             url=video_url,
#             event=event,
#             queue=queue,
#             size=video_size,
#             type_="video",
#             cid=cid
#         )
#
#         if not video:
#             return
#
#         queue.put({"status": Status.MERGE})
#
#         video_path = merge(
#             album=album,
#             audio=audio,
#             video=video,
#             name=name
#         )
#
#         queue.put({
#             "status": Status.DONE,
#             "video_path": os.path.normpath(video_path)
#         })
