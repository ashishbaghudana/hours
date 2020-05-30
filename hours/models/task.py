import datetime as dt
import peewee as pw
from .base import BaseModel


class Task(BaseModel):
    task_id = pw.AutoField()
    title = pw.CharField(max_length=255, help_text='Title of the task')
    description = pw.TextField(help_text='Description of the task', default='')
    status = pw.CharField(max_length=20,
                          choices=[
                              "planned", "in_progress", "blocked", "completed",
                              "abandoned"
                          ],
                          null=True,
                          index=True)
    created_time = pw.DateTimeField(
        formats=['%Y-%m-%d %H:%M:%S.%f', '%Y-%m-%d %H:%M:%S'],
        help_text='DateTime when task was created')
    start_time = pw.DateTimeField(
        formats=['%Y-%m-%d %H:%M:%S.%f', '%Y-%m-%d %H:%M:%S'],
        help_text='DateTime when task was started',
        null=True)
    completed_time = pw.DateTimeField(
        formats=['%Y-%m-%d %H:%M:%S.%f', '%Y-%m-%d %H:%M:%S'],
        help_text='DateTime when task was completed',
        null=True)
    due_date = pw.DateField(
        formats=['%Y-%m-%d %H:%M:%S.%f', '%Y-%m-%d %H:%M:%S'],
        index=True,
        help_text='Date when task is due',
        null=True)
    last_updated_time = pw.DateTimeField(
        formats=['%Y-%m-%d %H:%M:%S.%f', '%Y-%m-%d %H:%M:%S'],
        help_text='DateTime when task was updated',
        default=dt.datetime.now)
    expected_num_hours = pw.IntegerField(
        help_text='Expected number of hours to finish the task', default=None)


class TaskTagAssociation(BaseModel):
    task_id = pw.ForeignKeyField(Task,
                                 backref='tags',
                                 on_delete='CASCADE',
                                 index=True)
    tag = pw.CharField(help_text='Tag for the task', index=True)

    class Meta:
        primary_key = pw.CompositeKey('task_id', 'tag')


class TaskToChildTaskAssociation(BaseModel):
    task_id = pw.ForeignKeyField(Task, backref='child_tasks', index=True)
    child_task = pw.IntegerField(help_text='Child Task')


class TaskToParentTaskAssociation(BaseModel):
    task_id = pw.ForeignKeyField(Task,
                                 backref='parent_tasks',
                                 help_text='Task ID',
                                 index=True)
    parent_task = pw.IntegerField(help_text='Parent Task')
