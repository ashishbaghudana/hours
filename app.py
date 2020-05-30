import click
from flask import Flask
from flask_restful import Api

from hours.models import database, db_cli
from hours.resources import (TaskResource, TaskListResource, TaskTagResource,
                             TaskChildTaskResource, TaskParentTaskResource,
                             DayResource, DayListResource, EndDayResource,
                             TimeBlockResource, TimeBlockListResource,
                             TimeBlockEndResource)

app = Flask(__name__)
app.cli.add_command(db_cli)

api = Api(app, prefix='/api/v0.1')

# Get a list of tasks and create new tasks
api.add_resource(TaskListResource, '/tasks')
# Get, update, and delete task by ID
api.add_resource(TaskResource, '/task/<int:task_id>')
# Update and delete tags for a task
api.add_resource(TaskTagResource, '/task/<int:task_id>/tags')
# Update and delete child tasks for a task
api.add_resource(TaskChildTaskResource, '/task/<int:task_id>/child_tasks')
# Update and delete parent tasks for a task
api.add_resource(TaskParentTaskResource, '/task/<int:task_id>/parent_tasks')
# Create a new day and get a list of days?
api.add_resource(DayListResource, '/days')
# Get the day by date
api.add_resource(DayResource, '/day/<string:date>')
# End a day
api.add_resource(EndDayResource, '/day/<string:date>/end')
# Get a list of time blocks in a given day and create new time blocks
api.add_resource(TimeBlockListResource, '/day/<string:date>/timeblocks')
# Get details of a day block
api.add_resource(TimeBlockResource,
                 '/day/<string:date>/timeblock/<int:timeblock_id>')
# End a time block
api.add_resource(TimeBlockEndResource,
                 '/day/<string:date>/timeblock/<int:timeblock_id>/end')


@app.before_request
def before_request():
    database.connect()


@app.after_request
def after_request(response):
    database.close()
    return response


if __name__ == '__main__':
    app.run(debug=True)