from .DB import DB
from .BaseModel import db
from .VideoTable import Video


def create_table():
    db.connect()

    if not db.table_exists("video"):
        db.create_tables([Video])

    db.close()


create_table()
