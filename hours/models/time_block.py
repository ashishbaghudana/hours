import datetime as dt
import peewee as pw
from .base import BaseModel
from .task import Task


class TimeBlock(BaseModel):
    time_block_id = pw.IntegerField(
        help_text='Auto-incrementing timeblock ID field per day', index=True)
    start_time = pw.DateTimeField(help_text='Start time for the time block',
                                  default=dt.datetime.now)
    end_time = pw.DateTimeField(help_text='End time for the time block',
                                default=None,
                                null=True)
    activity_type = pw.CharField(
        help_text='The type of activity - can be task, meeting, break',
        default='task')
    task = pw.ForeignKeyField(Task)


class TimeBlockTagAssociation(BaseModel):
    time_block_id = pw.ForeignKeyField(Task,
                                 backref='tags',
                                 on_delete='CASCADE',
                                 index=True)
    tag = pw.CharField(help_text='Tag for the timeblock', index=True)

    class Meta:
        primary_key = pw.CompositeKey('time_block_id', 'tag')
