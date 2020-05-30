from marshmallow import Schema, fields, validate


class TaskSchema(Schema):
    task_id = fields.Int(required=True, dump_only=True)
    title = fields.Str(required=True)
    description = fields.Str()
    status = fields.Str(validate=validate.OneOf(
        ["planned", "in_progress", "blocked", "completed", "abandoned"]),
                        default=None)
    created_time = fields.DateTime('%Y-%m-%dT%H:%M:%S.%f',
                                   required=True,
                                   dump_only=True)
    start_time = fields.DateTime('%Y-%m-%dT%H:%M:%S.%f',
                                 default=None,
                                 allow_none=True)
    completed_time = fields.DateTime('%Y-%m-%dT%H:%M:%S.%f',
                                     default=None,
                                     allow_none=True)
    due_date = fields.Date(default=None, allow_none=True)
    expected_num_hours = fields.Int(default=None)
    tags = fields.Function(lambda obj: [c.tag for c in obj.tags], lambda tags: tags)
    child_tasks = fields.Function(
        lambda obj: [task.child_task for task in obj.child_tasks],
        lambda child_tasks: child_tasks)
    parent_tasks = fields.Function(
        lambda obj: [task.parent_task for task in obj.parent_tasks],
        lambda parent_tasks: parent_tasks)
