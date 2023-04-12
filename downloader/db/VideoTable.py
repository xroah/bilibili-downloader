from peewee import (
    CharField,
    IntegerField,
    DateTimeField,
    BooleanField,
    CompositeKey
)

from .BaseModel import BaseModel, db

date_format = "%Y-%m-%d %H:%M:%S"


class Video(BaseModel):
    bvid = CharField(max_length=20)
    aid = IntegerField()
    cid = IntegerField()
    season_id = IntegerField(null=True)
    page = IntegerField()
    multiple = BooleanField()
    title = CharField(max_length=100)
    create_time = DateTimeField(formats=date_format)
    finish_time = DateTimeField(formats=date_format, null=True)
    finished = BooleanField()

    class Meta:
        primary_key = CompositeKey("bvid", "cid")



