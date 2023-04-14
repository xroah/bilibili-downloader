from .BaseModel import db
from .PartTable import Part
from .VideoTable import Video
from .SeasonTable import Season
from .EpisodeTable import Episode


def create_table():
    db.connect()
    db.create_tables([Part, Video, Season, Episode])
    db.close()


create_table()
