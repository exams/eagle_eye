from flask_restful import Resource


class Foo(Resource):

    def get(self):
        return {'hello': 'world', "中国": "加油"}

    def post(self):
        pass
