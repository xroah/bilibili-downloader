from peewee import (
    CharField,
    IntegerField,
    DateTimeField,
    BooleanField,
    CompositeKey
)

from .BaseModel import BaseModel, date_format


class Part(BaseModel):
    bvid = CharField(max_length=20)
    aid = IntegerField()
    cid = IntegerField()
    path = CharField(max_length=200, null=True)
    season_id = IntegerField(null=True)
    page = IntegerField()
    multiple = BooleanField()
    title = CharField(max_length=100)
    quality = IntegerField(null=True)
    create_time = DateTimeField(formats=date_format)
    finish_time = DateTimeField(formats=date_format, null=True)
    finished = BooleanField()

    class Meta:
        primary_key = CompositeKey("bvid", "cid")
