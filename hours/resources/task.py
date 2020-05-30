import datetime as dt
import peewee as pw
from flask import request
from flask_restful import Resource
from marshmallow import ValidationError

from ..schemas import TaskSchema
from ..models import (database, Task, TaskTagAssociation,
                      TaskToChildTaskAssociation, TaskToParentTaskAssociation)

task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)


class TaskResource(Resource):
    def get(self, task_id):
        try:
            task = Task.get_by_id(task_id)
            return task_schema.dump(task), 200
        except pw.DoesNotExist:
            return {'error': 'Not found'}, 404

    def put(self, task_id):
        # Do not update tags, child_tasks, parent_tasks as part of this API 
        # call
        data = request.get_json()
        try:
            update_values = TaskSchema(partial=True).load(data)
            if set(update_values.keys()).intersection(
                ['tags', 'child_tasks', 'parent_tasks']):
                return {
                    'error':
                    'Updating tags, child_tasks, and parent_tasks should happen through their respective APIs'
                }, 400
            Task.update(**update_values).where(Task.task_id == task_id).execute()
            return task_schema.dump(Task.get_by_id(task_id)), 201
        except pw.DoesNotExist:
            return {'error': 'Not found'}, 404
        except ValidationError as err:
            return {'errors': err.messages}, 400

    def delete(self, task_id):
        try:
            Task.delete_by_id(task_id)
        except pw.DoesNotExist:
            return {'error': 'Not found'}, 404
        return {'id': task_id, 'success': True}, 201


class TaskListResource(Resource):
    def get(self):
        tasks = list(Task.select())
        return {'tasks': tasks_schema.dump(tasks)}, 200

    def post(self):
        data = request.get_json()
        try:
            task = task_schema.load(data)
            task = Task.create(created_time=dt.datetime.now(), **task)
        except ValidationError as err:
            return {'errors': err.messages}, 400
        return task_schema.dump(task), 201


class TaskTagResource(Resource):
    def post(self, task_id):
        data = request.get_json()
        data_source = [{
            'task_id': task_id,
            'tag': tag
        } for tag in data['tags']]
        query = TaskTagAssociation.select().where(
            TaskTagAssociation.task_id == task_id)
        results = list(query)
        existing_tags = [result.tag for result in results]
        intersection = set(existing_tags).intersection(data['tags'])
        if (len(intersection) > 0):
            return {
                'success':
                False,
                'errors':
                f'Duplicate value(s) -- {", ".join(intersection)} -- not allowed'
            }, 400
        with database.atomic():
            TaskTagAssociation.insert_many(data_source).execute()
        task = Task.get_by_id(task_id)
        return task_schema.dump(task), 201

    def delete(self, task_id):
        data = request.get_json()
        with database.atomic():
            TaskTagAssociation.delete().where(
                (TaskTagAssociation.task_id == task_id)
                & TaskTagAssociation.tag.in_(data['tags'])).execute()
        task = Task.get_by_id(task_id)
        return task_schema.dump(task), 201


class TaskChildTaskResource(Resource):
    def post(self, task_id):
        data = request.get_json()
        data_source_child = [{
            'task_id': task_id,
            'child_task': child_task
        } for child_task in data['tasks']]
        data_source_parent = [{
            'task_id': child_task,
            'parent_task': task_id
        } for child_task in data['tasks']]
        query = TaskToChildTaskAssociation.select().where(
            TaskToChildTaskAssociation.task_id == task_id)
        results = list(query)
        existing_tasks = [result.child_task for result in results]
        intersection = set(existing_tasks).intersection(data['tasks'])
        if (len(intersection) > 0):
            return {
                'success':
                False,
                'errors':
                f'Duplicate value(s) -- {", ".join(intersection)} -- not allowed'
            }, 400
        with database.atomic():
            TaskToChildTaskAssociation.insert_many(data_source_child).execute()
            TaskToParentTaskAssociation.insert_many(data_source_parent).execute()
        task = Task.get_by_id(task_id)
        return task_schema.dump(task), 201

    def delete(self, task_id):
        data = request.get_json()
        with database.atomic():
            TaskToChildTaskAssociation.delete().where(
                (TaskToChildTaskAssociation.task_id == task_id)
                & TaskToChildTaskAssociation.child_task.in_(data['tasks'])
            ).execute()
            TaskToParentTaskAssociation.delete().where(
                (TaskToParentTaskAssociation.task_id.in_(data['tasks']))
                & (TaskToParentTaskAssociation.parent_task == task_id)
            ).execute()
        task = Task.get_by_id(task_id)
        return task_schema.dump(task), 201


class TaskParentTaskResource(Resource):
    def post(self, task_id):
        data = request.get_json()
        data_source_parent = [{
            'task_id': task_id,
            'parent_task': parent_task
        } for parent_task in data['tasks']]
        data_source_child = [{
            'task_id': parent_task,
            'child_task': task_id
        } for parent_task in data['tasks']]
        query = TaskToParentTaskAssociation.select().where(
            TaskToChildTaskAssociation.task_id == task_id)
        results = list(query)
        existing_tasks = [result.parent_task for result in results]
        intersection = set(existing_tasks).intersection(data['tasks'])
        if (len(intersection) > 0):
            return {
                'success':
                False,
                'errors':
                f'Duplicate value(s) -- {", ".join(intersection)} -- not allowed'
            }, 400
        with database.atomic():
            TaskToParentTaskAssociation.insert_many(data_source_parent).execute()
            TaskToChildTaskAssociation.insert_many(data_source_child).execute()
        task = Task.get_by_id(task_id)
        return task_schema.dump(task), 201

    def delete(self, task_id):
        data = request.get_json()
        with database.atomic():
            TaskToChildTaskAssociation.delete().where(
                (TaskToChildTaskAssociation.task_id == task_id)
                & TaskToChildTaskAssociation.parent_task.in_(data['tasks'])
            ).execute()
            TaskToParentTaskAssociation.delete().where(
                (TaskToParentTaskAssociation.task_id.in_(data['tasks']))
                & (TaskToParentTaskAssociation.child_task == task_id)
            ).execute()
        task = Task.get_by_id(task_id)
        return task_schema.dump(task), 201