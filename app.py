from flask import Flask
from flask_restful import Api
from flask_pymongo import PyMongo
from resources.foo import Foo
from resources.papers import Papers

app = Flask(__name__)
api = Api(app)

app.config.update(
    MONGO_URI='mongodb://localhost:27017/mean-dev'
)
mongo = PyMongo(app)


api.add_resource(Foo, '/Foo')

if __name__ == '__main__':
    app.run(debug=True)
