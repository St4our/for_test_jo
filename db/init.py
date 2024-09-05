import logging

from db.db import db
from db.models import Plan, Task, PlanHistory


def init():
    logging.critical('Create tables')
    models = [Plan, PlanHistory, Task]
    db.create_tables(models=models)
