import datetime as dt
import peewee as pw
from flask import request
from flask_restful import Resource
from marshmallow import ValidationError

from ..schemas import DaySchema
from ..models import (database, Day, DayTimeBlockAssociation)


day_schema = DaySchema()
days_schema = DaySchema(many=True)


class DayResource(Resource):
    def get(self, date):
        date_obj = dt.datetime.strptime(date, '%Y-%m-%d')
        try:
            day = Day.get(Day.friendly_date == date_obj)
            return day_schema.dump(day)
        except pw.DoesNotExist:
            return {'error': 'Not found'}, 404

    def delete(self, date):
        date_obj = dt.datetime.strptime(date, '%Y-%m-%d')
        with database.atomic():
            Day.delete().where(Day.friendly_date == date_obj).execute()
        return {'success': True}, 201


class DayListResource(Resource):
    def post(self):
        data = request.get_json()
        today = dt.datetime.today()
        if data is not None and 'friendly_date' in data:
            today = dt.datetime.strptime(data['friendly_date'], '%Y-%m-%d')
        day = Day.get_or_none(Day.friendly_date == today)
        if day is not None:
            return {
                'error': 'Already created day for today, delete and try again'
            }, 400
        Day.create(friendly_date=today)
        day = Day.get(Day.friendly_date == today)
        return day_schema.dump(day), 200

    def get(self):
        args = request.args
        if ('start_date' not in args or 'end_date' not in args):
            return {
                'error':
                'Query parameters must contain start_date and end_date'
            }, 400
        start_date = dt.datetime.strptime(args['start_date'], '%Y-%m-%d')
        end_date = dt.datetime.strptime(args['end_date'], '%Y-%m-%d')
        days = Day.select().where(Day.friendly_date.between(start_date, end_date)).order_by(Day.friendly_date.desc())
        return days_schema.dump(days), 200


class EndDayResource(Resource):
    def post(self, date):
        date_obj = dt.datetime.strptime(date, '%Y-%m-%d')
        try:
            day = Day.get(Day.friendly_date == date_obj)
            day.end_time = dt.datetime.now()
            day.save()
            return day_schema.dump(day)
        except pw.DoesNotExist:
            return {'Not found'}, 404
