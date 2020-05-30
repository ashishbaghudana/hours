from marshmallow import Schema, fields, validate, validates_schema, ValidationError, pre_load
from .task import TaskSchema


class TimeBlockSchema(Schema):
    start_time = fields.DateTime(required=True)
    end_time = fields.DateTime()
    activity_type = fields.Str(validate=validate.OneOf(
        ['task', 'meeting', 'break']),
                               required=True)
    task = fields.Nested(TaskSchema(only=['task_id', 'title', 'description']))
    tags = fields.List(fields.Str())

    @validates_schema
    def validate_activity_type(self, data, **kwargs):
        if (data['activity_type'] == 'task'):
            try:
                assert (data['task'] is not None)
            except:
                raise ValidationError(
                    'Task should be set if activity type is "task"')

    @pre_load
    def lowercase_tags(self, data, **kwargs):
        data['tags'] = [tag.lower() for tag in data['tags']]
        return data
