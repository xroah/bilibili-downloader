import sqlite3
import os
from typing import Callable

from ..utils import utils
from ..utils.Singleton import Singleton


class DB(Singleton):
    def __init__(self) -> None:
        data_dir = utils.get_data_dir()
        path = os.path.join(data_dir, "data.db")
        self._conn = sqlite3.connect(path)
        self._conn.row_factory = sqlite3.Row
        self._cursor = self._conn.cursor()

    def __enter__(self):
        self.create_table()
        return self

    def __exit__(self, t, v, tb):
        self._conn.commit()
        self._cursor.close()
        self._conn.close()

        if t is not None:
            return False

    def create_table(self):
        self._cursor.execute("""
            CREATE TABLE IF NOT EXISTS download(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                vid VARCHAR(20),
                cid UNSIGNED INT,
                size UNSIGNED INT,
                name VARCHAR(200),
                status UNSIGNED tinyint,
                create_time DATETIME,
                finished_time DATETIME
            )
        """)
        self._cursor.execute("""
            CREATE TABLE IF NOT EXISTS album(
                vid VARCHAR(20) PRIMARY KEY,
                aid UNSIGNED INT,
                name VARCHAR(200),
                quality UNSIGNED SMALLINT,
                create_time DATETIME
            )
        """)

    def query_all(self, vid: str = ""):
        where = f"WHERE vid='{id}'" if vid else ""
        r = self._cursor.execute(f"""
            SELECT d.vid, d.name, d.cid, d.status, 
            a.quality, a.name album, a.aid
            FROM download d LEFT OUTER JOIN album a 
            USING (vid) {where};
        """)

        return r.fetchall()

    def insert(self, data, cb: Callable = None):
        bvid = data["bvid"]
        ret = self._cursor.execute(
            f"SELECT vid FROM album WHERE vid='{bvid}'"
        )
        album = data["title"]
        exists = []
        quality = data["quality"]

        # exists
        if ret.fetchone():
            exists = self._cursor.execute(
                f"SELECT cid FROM download WHERE vid='{bvid}'"
            ).fetchall()
            exists = list(map(lambda d: d[0], exists))

        now = 'datetime("now", "localtime")'
        video_clause = f"""
            INSERT INTO download(
                vid, cid, size, name, status, create_time
            ) VALUES(?, ?, ?, ?, ?, {now})
        """
        pages = data["pages"]
        insertion_list = []
        videos = []

        for v in pages:
            if v["cid"] not in exists:
                video = {
                    "cid": v["cid"],
                    "name": v["part"],
                    "album": album,
                    "quality": quality,
                    "status": 0,
                    "vid": bvid,
                    "aid": data["avid"]
                }
                videos.append(video)
                insertion_list.append(
                    (f'{bvid}', v["cid"], 0, f'{v["part"]}', 0)
                )

        album_clause = f"""
            INSERT INTO album(vid, aid, name, quality, create_time) 
            VALUES('{bvid}', '{data["avid"]}', '{album}',
             {quality}, {now})
        """

        if not len(exists):
            self._cursor.execute(album_clause)
            self._cursor.executemany(video_clause, insertion_list)

            if cb:
                cb(videos)