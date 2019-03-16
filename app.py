from flask import Flask
from flask_restful import Api
from resources.foo import Foo
from resources.papers import Papers

app = Flask(__name__)
api = Api(app)

api.add_resource(Foo, '/Foo')

if __name__ == '__main__':
    app.run(debug=True)
