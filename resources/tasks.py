from flask_restful import fields, marshal_with, reqparse, Resource


post_parser = reqparse.RequestParser()
post_parser.add_argument(
    'name', required=True,
    help='The task\'s username',
)

task_fields = {
    'name': fields.String,
    'process': fields.Integer
}

class Tasks(Resource):

    def get(self):
        pass

    @marshal_with(task_fields)
    def post(self):
        args = post_parser.parse_args()
        return args


class Task(Resource):

    def get(self, task_id):
        return {task_id: task_id}


    def delete(self, task_id):
        pass


