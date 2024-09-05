import datetime

from peewee import PrimaryKeyField, CharField, DateTimeField

from db.models import BaseModel


class Task(BaseModel):
    class Meta:
        db_table = 'tasks'

    id = PrimaryKeyField()
    name = CharField(max_length=128)
    created = DateTimeField(default=datetime.datetime.now)
