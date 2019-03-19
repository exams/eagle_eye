from flask_restful import fields, marshal_with, reqparse, Resource
from app import mongo


post_parser = reqparse.RequestParser()
task_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'process': fields.Integer
}

class Tasks(Resource):

    def get(self):
        pass

    @marshal_with(task_fields)
    def post(self):
        args = post_parser.parse_args()
        mongo.db.tasks.save()
        pass
