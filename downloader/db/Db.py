import sqlite3
import os

from ..utils import utils
from ..utils.Singleton import Singleton


class Db(Singleton):
    def __init__(self) -> None:
        data_dir = utils.get_data_dir()
        self.path = os.path.join(data_dir, "data.db")
        self.create_table()
        

    def create_table(self):
        conn = sqlite3.connect(self.path)
        conn.execute("""
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
        conn.execute("""
            CREATE TABLE IF NOT EXISTS album(
                vid VARCHAR(20) PRIMARY KEY,
                aid UNSIGNED INT,
                name VARCHAR(200),
                quality UNSIGNED SMALLINT,
                create_time DATETIME
            )
        """)
        conn.commit()
        conn.close()

    def insert_data(self, data):
        conn = sqlite3.connect(self.path)
        video_clause = """
            INSERT INTO download(
                vid, cid, size, title, status, create_time
            ) VALUES
        """
        video_values = []
        first = data[0]
        album_clause = """
            INSERT INTO album(vid, aid, name, quality, create_time) 
            VALUES('{0}', '{1}', '{2}', {3}, datetime("now", "localtime"))
        """.format(first["vid"], first["aid"], first["album"], first["quality"])

        for v in data:
            video_values.append(f"""(
                '{v["vid"]}', {v["cid"]}, 0,'{v["part"]}', 0,
                datetime("now", "localtime")
            )""")

        video_clause += ",".join(video_values)
        conn.execute(album_clause)
        conn.execute(video_clause)
        conn.commit()
        conn.close()

