from peewee import CharField, DateTimeField

from .BaseModel import BaseModel, date_format


class Video(BaseModel):
    bvid = CharField(max_length=20, primary_key=True)
    title = CharField(max_length=100)
    create_time = DateTimeField(formats=date_format)