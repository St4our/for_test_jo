from peewee import Model

from db.db import db


class BaseModel(Model):
    class Meta:
        db_table = 'base'
        database = db
