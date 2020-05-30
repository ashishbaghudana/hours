import click
from flask.cli import AppGroup

from .base import mysql_db as database
from .task import (Task, TaskTagAssociation, TaskToChildTaskAssociation,
                   TaskToParentTaskAssociation)
from .time_block import TimeBlock, TimeBlockTagAssociation
from .day import Day, DayTimeBlockAssociation

TABLES = [
    Task, TaskTagAssociation, TaskToChildTaskAssociation,
    TaskToParentTaskAssociation, TimeBlock, TimeBlockTagAssociation,
    Day, DayTimeBlockAssociation
]

db_cli = AppGroup('db')


@db_cli.command('drop-tables')
def drop_tables():
    with database:
        database.drop_tables(TABLES)


@db_cli.command('create-tables')
def create_tables():
    with database:
        database.create_tables(TABLES)