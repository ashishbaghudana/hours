import datetime as dt
import peewee as pw
from flask import request
from flask_restful import Resource
from marshmallow import ValidationError

from ..schemas import TimeBlockSchema
from ..models import (database, Day, TimeBlock, TimeBlockTagAssociation)

time_block_schema = TimeBlockSchema()
time_blocks_schema = TimeBlockSchema(many=True)


class TimeBlockResource(Resource):
    def get(self, timeblock_id):
        try:
            time_block = TimeBlock.get_by_id(timeblock_id)
            return time_block_schema.dump(time_block), 200
        except pw.DoesNotExist:
            return {'error': 'Not found'}, 404


class TimeBlockEndResource(Resource):
    def post(self, day, timeblock_id):
        try:
            date = dt.datetime.strptime(day, '%Y-%m-%d')
            day = Day.select().where(Day.friendly_date == date)
            time_blocks = day.time_blocks
            if timeblock_id > len(time_blocks):
                return {'error': 'Time block does not exist'}
            time_block = time_blocks[timeblock_id - 1]
            if time_block.end_time is not None:
                return {'error': 'Time block has already ended'}, 400
            time_block.end_time = dt.datetime.now()
            time_block.save()
            return time_block_schema.dump(time_block)
        except pw.DoesNotExist:
            return {'error': 'Not found'}, 404


class TimeBlockListResource(Resource):
    def post(self, day):
        data = request.get_json()
        try:
            parsed_data = time_block_schema.load(data)
            parsed_data['start_time'] = dt.datetime.now()
            tags = parsed_data.pop('tags', None)
        except ValidationError as err:
            return {'errors': err.messages}, 400

    # def get(self, day):
    #     day =
