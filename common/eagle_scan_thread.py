import threading
import os
import cv2
from common import platform_os_type
from common.config import windows_store_prefix, linux_store_prefix
import datetime
import numpy as np


class EagleScanThread(threading.Thread):

    def __init__(self, task):
        super(EagleScanThread, self).__init__()
        self.task = task

    def run(self):
        # 根据操作系统路径前缀和年月日以及试卷id生成试卷电子化保存的路径
        today = datetime.date.today()
        if platform_os_type.lower().index('windows') >= 0:
            store_path = windows_store_prefix + str(today.year) + os.sep + str(today.month) + os.sep + str(today.day) + os.sep
        elif platform_os_type.lower().index('linux') >= 0:
            store_path = linux_store_prefix + str(today.year) + os.sep + str(today.month) + os.sep + str(today.day) + os.sep

        print(store_path)
        # 判断目录是否存在, 不存在则创建.
        is_exists = os.path.exists(store_path)
        if not is_exists:
            os.makedirs(store_path)

        work_path = self.task.path
        dirs = os.listdir(work_path)
        for file in dirs:
            print(work_path + os.sep + file)
            image = cv2.imread(work_path + os.sep + file, cv2.IMREAD_COLOR)
            print(image)
