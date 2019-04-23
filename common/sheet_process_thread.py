import threading
import os
import cv2
from common import platform_os_type
from common.config import windows_store_prefix, linux_store_prefix
import datetime
import numpy as np
import filetype
import io
from wand.image import Image
from wand.color import Color
from PyPDF2 import PdfFileReader, PdfFileWriter


class SheetProcessThread(threading.Thread):

    def __init__(self, task):
        super(SheetProcessThread, self).__init__()
        self.task = task

    # 抓换pdf文件为图片
    def _convert_pdf2img(self, file, work_path, temp_store_path):
        file_name = work_path + os.sep + file
        pdf_file = PdfFileReader(file_name, strict=False)
        pageObj = pdf_file.getPage(0)
        dst_pdf = PdfFileWriter()
        dst_pdf.addPage(pageObj)
        pdf_bytes = io.BytesIO()
        dst_pdf.write(pdf_bytes)
        pdf_bytes.seek(0)

        img = Image(file=pdf_bytes, resolution=200)
        img.format = 'jpg'
        img.compression_quality = 90
        img.background_color = Color("white")
        img_path = temp_store_path + os.sep + '%s.jpg' % (file[:file_name.rindex('.')])
        img.save(filename=img_path)
        img.destroy()

    # 对图片进行旋转.

    # 对图片进行处理
    def shape(self, file):
        img = cv2.imread(file)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
        cv2.imshow("input image", img)

        if cv2.waitKey(0) & 0xff ==27:
            cv2.destroyAllWindows()

        out_binary, contours, hierarchy = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(img, contours, -1, (0, 255, 0), 1)

        cv2.imshow("input image", img)
        if cv2.waitKey(0) & 0xff ==27:
            cv2.destroyAllWindows()

        for cnt in range(len(contours)):
            epsilon = 0.01 * cv2.arcLength(contours[cnt], True)
            approx = cv2.approxPolyDP(contours[cnt], epsilon, True)

            corners = len(approx)
            if corners == 4:
                print(approx[0][0])


    def run(self):
        # 根据操作系统路径前缀和年月日以及试卷id生成试卷电子化保存的路径
        today = datetime.date.today()
        if platform_os_type.lower().index('windows') >= 0:
            store_path = windows_store_prefix + str(today.year) + os.sep + str(today.month) + os.sep + str(today.day) + os.sep
        elif platform_os_type.lower().index('linux') >= 0:
            store_path = linux_store_prefix + str(today.year) + os.sep + str(today.month) + os.sep + str(today.day) + os.sep

        temp_store_path = store_path + os.sep + self.task.paper_id
        # 判断目录是否存在, 不存在则创建.
        is_exists = os.path.exists(temp_store_path)
        if not is_exists:
            os.makedirs(temp_store_path)

        work_path = self.task.path
        dirs = os.listdir(work_path)

        # 先将文件整理到临时存储目录,包括对格式的转换. 旋转,以及图像处理
        for file in dirs:
            file_name = work_path + os.sep + file
            file_type = filetype.guess(file_name)
            if filetype is None:
                print("Cannot guass file type!")
                continue
            print(work_path + os.sep + file)

            # 如果扫描文件是pdf格式的, 则需要先转换为图像.
            if file_type.extension == 'pdf':
                self._convert_pdf2img(file, work_path, temp_store_path)

        temp_file_list = os.listdir(temp_store_path)
        for file in temp_file_list:
            file_name = temp_store_path + os.sep + file
            self.shape(file_name)
