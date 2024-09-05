import datetime

from peewee import PrimaryKeyField, CharField, BigIntegerField, DateTimeField

from db.models import BaseModel


class Plan(BaseModel):
    class Meta:
        db_table = 'plans'

    id = PrimaryKeyField()
    name = CharField(max_length=128)
    plan_month_value = BigIntegerField(default=0)
    plan_month = BigIntegerField(default=0)
    fact_month = BigIntegerField(default=0)
    fact_day = BigIntegerField(default=0)
    created = DateTimeField(default=datetime.datetime.now)
