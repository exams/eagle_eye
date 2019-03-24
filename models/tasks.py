from common import db
from mongoengine import *
import datetime


# 类名定义 collection
class Task(db.Document):
    # 字段
    name = db.StringField(max_length=30, required=True)
    path = db.StringField()
    pieces = db.IntField(min_value=0)
    processed = db.IntField(min_value=0, default=0)
    create_time = DateTimeField(default=datetime.datetime.utcnow)
    progress = db.IntField(min_value=0, max_value=100, default=0)
    finish_time = DateTimeField()


