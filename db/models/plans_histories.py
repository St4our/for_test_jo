import datetime

from peewee import PrimaryKeyField, CharField, BigIntegerField, DateTimeField

from db.models import BaseModel


class PlanHistory(BaseModel):
    class Meta:
        db_table = 'plans_histories'

    id = PrimaryKeyField()
    name = CharField(max_length=128)
    fact_day = BigIntegerField(default=0)
    created = DateTimeField(default=datetime.datetime.now)
