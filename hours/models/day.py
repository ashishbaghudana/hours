import datetime as dt
import peewee as pw
from .base import BaseModel
from .time_block import TimeBlock


class Day(BaseModel):
    friendly_date = pw.DateField(formats=['%Y-%m-%d'],
                                 help_text='The day being recorded',
                                 default=dt.datetime.today,
                                 index=True)
    start_time = pw.DateTimeField(help_text='Start time for the day',
                                  default=dt.datetime.now)
    end_time = pw.DateTimeField(help_text='End time for the day',
                                default=None,
                                null=True)


class DayTimeBlockAssociation(BaseModel):
    day_id = pw.ForeignKeyField(Day,
                                backref='time_blocks',
                                on_delete='CASCADE')
    time_block = pw.ForeignKeyField(TimeBlock, help_text='Timeblock ID')

    class Meta:
        primary_key = pw.CompositeKey('day_id', 'time_block')
