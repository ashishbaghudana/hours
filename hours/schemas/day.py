from marshmallow import Schema, fields, validate
from .time_block import TimeBlockSchema


class DaySchema(Schema):
    friendly_date = fields.Date(required=True,
                                help_text='Date for the day',
                                dump_only=True)
    start_time = fields.DateTime(required=True,
                                 help_text='Start time for the day',
                                 dump_only=True)
    end_time = fields.DateTime(help_text='End time for the day')
    time_blocks = fields.List(fields.Nested(TimeBlockSchema()), dump_only=True)