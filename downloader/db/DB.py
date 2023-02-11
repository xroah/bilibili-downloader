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
        self.create_table()

    def __enter__(self):
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
                path VARCHAR(1000),
                name VARCHAR(200),
                status UNSIGNED tinyint,
                create_time DATETIME,
                finish_time DATETIME
            );
        """)
        self._cursor.execute("""
            CREATE TABLE IF NOT EXISTS album(
                vid VARCHAR(20) PRIMARY KEY,
                aid UNSIGNED INT,
                name VARCHAR(200),
                quality UNSIGNED SMALLINT,
                create_time DATETIME
            );
        """)

    def query_all(self, vid: str = ""):
        where = f"WHERE vid='{id}'" if vid else ""
        r = self._cursor.execute(f"""
            SELECT d.vid, d.name, d.path, d.cid, d.status, d.size,
            d.finish_time, a.quality, a.name album, a.aid
            FROM download d LEFT OUTER JOIN album a 
            USING (vid) {where} ORDER BY d.finish_time;
        """)

        return r.fetchall()

    def delete_rows(self, cids: tuple):
        self._cursor.execute(f"""
            DELETE FROM download WHERE cid in ({",".join(cids)});
        """)

    def update_finished(self, cid: int, path: str):
        self._cursor.execute(f"""
            UPDATE download SET finish_time=datetime('now', 'localtime'),
            path='{path}', status=1 WHERE cid={cid};
        """)

    def update_size(self, cid: int, size: int):
        self._cursor.execute(f"""
            UPDATE download SET size='{size}' WHERE cid={cid};
        """)

    def insert(self, data, cb: Callable = None):
        bvid = data["bvid"]
        exist_album = self._cursor.execute(
            f"SELECT vid FROM album WHERE vid='{bvid}';"
        ).fetchone()
        album = data["title"]
        exists = []
        quality = data["quality"]

        # exists
        if exist_album:
            exists = self._cursor.execute(
                f"SELECT cid FROM download WHERE vid='{bvid}';"
            ).fetchall()
            exists = list(map(lambda d: d[0], exists))

        now = 'datetime("now", "localtime")'
        video_clause = f"""
            INSERT INTO download(
                vid, cid, size, name, status, create_time
            ) VALUES(?, ?, ?, ?, ?, {now});
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
             {quality}, {now});
        """

        if len(videos):
            if not exist_album:
                self._cursor.execute(album_clause)
            self._cursor.executemany(video_clause, insertion_list)

        if cb:
            cb(videos)
