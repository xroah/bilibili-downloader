import sqlite3
import os

from ..utils import utils
from ..utils.Singleton import Singleton


class DB(Singleton):
    def __init__(self) -> None:
        data_dir = utils.get_data_dir()
        path = os.path.join(data_dir, "data.db")
        self.conn = sqlite3.connect(path)
        self.cursor = self.conn.cursor()
        
    def __enter__(self):
        self.create_table()
        return self

    def __exit__(self, t, v, tb):
        self.conn.commit()
        self.conn.close()

        if t is not None:
            return False

    def create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS download(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                vid VARCHAR(20),
                cid UNSIGNED INT,
                size UNSIGNED INT,
                title VARCHAR(200),
                status UNSIGNED tinyint,
                create_time DATETIME,
                finished_time DATETIME
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS album(
                vid VARCHAR(20) PRIMARY KEY,
                aid UNSIGNED INT,
                name VARCHAR(200),
                quality UNSIGNED SMALLINT,
                create_time DATETIME
            )
        """)
    
    def insert(self, data):
        now = 'datetime("now", "localtime")'
        video_clause = f"""
            INSERT INTO download(
                vid, cid, size, title, status, create_time
            ) VALUES(?, ?, ?, ?, ?, {now})
        """
        videos = list(map(
            lambda v: (
                f'{data["bvid"]}', v["cid"], 0, f'{v["part"]}', 0
            ),
            data["pages"]
        ))
        album_clause = f"""
            INSERT INTO album(vid, aid, name, quality, create_time) 
            VALUES('{data["bvid"]}', '{data["avid"]}', '{data["title"]}',
             {data["quality"]}, {now})
        """

        self.cursor.execute(album_clause)
        self.cursor.executemany(video_clause, videos)

