from peewee import (
    CharField,
    IntegerField,
    DateField,
    BooleanField
)

from .BaseModel import BaseModel, date_format


class Episode(BaseModel):
    ep_id = IntegerField(primary_key=True)
    aid = IntegerField()
    cid = IntegerField()
    bvid = CharField(max_length=20)
    title = CharField(max_length=100)
    create_time = DateField(formats=date_format)
    path = CharField(max_length=200, null=True)
    quality = IntegerField(null=True)
    finished = BooleanField()
    finish_time = DateField(formats=date_format, null=True)
