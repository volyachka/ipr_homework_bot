from peewee import *
from settings import db_filename

db = SqliteDatabase(db_filename)


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    id = CharField(default='')
    tg_id = IntegerField(default=0)
    tg_username = CharField(default='')
    country = CharField(default='')
    city = CharField(default='')
    categories = TextField(default='')
    frequency_of_mailing = CharField(default='')
    tracking_method = CharField(default='')
    mode = CharField(default='need to fill tg_id and username')

