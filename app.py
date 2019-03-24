from common import app
from flask_restful import Api
from resources.foo import Foo
from resources.tasks import TasksApi, TaskApi

api = Api(app)

api.add_resource(Foo, '/Foo')
api.add_resource(TasksApi, '/tasks')
api.add_resource(TaskApi, '/task/<string:task_id>')

if __name__ == '__main__':
    app.run(debug=True)
