from peewee import DateTimeField, CharField, IntegerField

from .BaseModel import BaseModel, date_format


class Season(BaseModel):
    season_id = IntegerField(primary_key=True)
    title = CharField(max_length=100)
    create_time = DateTimeField(formats=date_format)
