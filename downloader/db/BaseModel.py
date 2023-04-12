from peewee import Model, SqliteDatabase
import os.path

from ..utils import utils

_db_path = os.path.join(utils.get_data_dir(), "data.db")
db = SqliteDatabase(
    _db_path,
    pragmas={
        "journal_mode": "wal",
        "cache_size": -1 * 32000
    }
)


class BaseModel(Model):
    class Meta:
        database = db

