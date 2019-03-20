from app import db
from mongoengine import *
import datetime

# 类名定义 collection
class Task(db.Document):
    # 字段
    name = db.StringField(max_length=30, required=True)
    path = db.StringField()
    create_time = DateTimeField(default=datetime.datetime.utcnow)
    process = db.IntField(min_value=0, max_value=100)
    finish_time = DateTimeField()


