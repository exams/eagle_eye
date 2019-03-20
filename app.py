from flask import Flask
from flask_restful import Api
from flask_mongoengine import MongoEngine
from resources.foo import Foo
from resources.tasks import Tasks, Task
from resources.papers import Papers

app = Flask(__name__)
api = Api(app)

app.config['MONGODB_SETTINGS'] = {
    'db':   'todoApp',
    'host': '127.0.0.1',
    'port': 27017
}

#app.config.from_pyfile('config.json')
db = MongoEngine(app)


api.add_resource(Foo, '/Foo')
api.add_resource(Tasks, '/tasks')
api.add_resource(Task, '/task/<string:task_id>')

if __name__ == '__main__':
    app.run(debug=True)
