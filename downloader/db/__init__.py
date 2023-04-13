from .BaseModel import db
from .PartTable import Part
from .VideoTable import Video
from .SeasonTable import Season


def create_table():
    db.connect()
    db.create_tables([Part, Video, Season])
    db.close()


create_table()
