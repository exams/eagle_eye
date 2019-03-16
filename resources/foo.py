from flask_restful import Resource


class Foo(Resource):

    def get(self):
        return {'hello': 'world'}

    def post(self):
        pass
