import threading
import os
from common.sheet_process_thread import SheetProcessThread


class EagleScanThread(threading.Thread):

    def __init__(self, task):
        super(EagleScanThread, self).__init__()
        self.task = task

    def run(self):
        work_path = self.task.path
        dirs = os.listdir(work_path)

        # 设置线程池,将所有文件提交线程池处理
        for file in dirs:
            file_name = work_path + os.sep + file
            t = SheetProcessThread(file_name)
            t.start()

