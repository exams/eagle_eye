from flask_restful import fields, marshal_with, reqparse, Resource
from models.tasks import Task
from common import platform_os_type
from common.config import windows_temp_store_prefix, linux_temp_store_prefix
import os
from common.eagle_scan_thread import EagleScanThread


post_parser = reqparse.RequestParser()
post_parser.add_argument(
    'name', required=True,
    help='The task\'s username',
)
post_parser.add_argument(
    'paper_id', required=True,
    help='The paper\'s id',
)

task_fields = {
    '_id': fields.String,
    'name': fields.String,
    'process': fields.Integer,
    'pieces': fields.Integer,
    'processed': fields.Integer,
    'progress': fields.Integer,
    'create_time': fields.DateTime
}


class TasksApi(Resource):

    def get(self):
        pass

    @marshal_with(task_fields)
    def post(self):
        args = post_parser.parse_args()
        task = Task()
        # task name 根据试卷名称生成
        task.name = args.name
        # 路径根据操作系统路径前缀和试卷id生成
        if platform_os_type.lower().index('windows') >= 0:
            task.path = windows_temp_store_prefix + args.paper_id
        elif platform_os_type.lower().index('linux') >= 0:
            task.path = linux_temp_store_prefix + args.paper_id

        # 将ftp目录拷贝至生成的临时目录

        # 读取新生成的目录下的文件数量
        task.pieces = len(os.listdir(task.path))

        task = task.save()
        # 任务保存完成后,启动线程处理任务
        t = EagleScanThread(task)
        t.start()

        return task


class TaskApi(Resource):

    def get(self, task_id):
        return {task_id: task_id}

    def delete(self, task_id):
        pass


