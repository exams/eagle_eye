from flask import Flask
from flask_mongoengine import MongoEngine
import platform

app = Flask(__name__)

app.config['MONGODB_SETTINGS'] = {
    'db':   'mean-dev',
    'host': '127.0.0.1',
    'port': 27017
}

db = MongoEngine(app)
platform_os_type = platform.system()
