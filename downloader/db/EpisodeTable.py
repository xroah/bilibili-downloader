from peewee import (
    CharField,
    IntegerField,
    DateField,
    BooleanField,
    CompositeKey
)

from .BaseModel import BaseModel, date_format


class Episode(BaseModel):
    ep_id = IntegerField()
    aid = IntegerField()
    cid = IntegerField()
    bvid = CharField(max_length=20)
    season_id = IntegerField()
    title = CharField(max_length=100)
    create_time = DateField(formats=date_format)
    path = CharField(max_length=200, null=True)
    quality = IntegerField(null=True)
    finished = BooleanField()
    finish_time = DateField(formats=date_format, null=True)

    class Meta:
        primary_key = CompositeKey("aid", "ep_id")
