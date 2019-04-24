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
import uuid



class SheetProcessThread(threading.Thread):

    def __init__(self, sheet_file):
        super(SheetProcessThread, self).__init__()
        self.sheet_file = sheet_file

    # 转换pdf文件为图片
    def _convert_pdf2img(self, file, store_path):
        pdf_file = PdfFileReader(file, strict=False)
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
        img_path = store_path + '%s.jpg' % (uuid.uuid3(uuid.uuid1(), file))
        print(img_path)
        img.save(filename=img_path)
        img.destroy()
        return img_path

    # 对图片进行旋转.
    def _rotate(self, img):
        pass

    # 对图片进行位置提取处理
    @staticmethod
    def _extract_shape(file):
        img = cv2.imread(file)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)

        out_binary, contours, hierarchy = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for cnt in range(len(contours)):
            epsilon = 0.01 * cv2.arcLength(contours[cnt], True)
            approx = cv2.approxPolyDP(contours[cnt], epsilon, True)

            corners = len(approx)
            if corners == 4:
                print(approx[0][0])
                rect = cv2.minAreaRect(approx)
                print(rect)
                # cv2.imshow("input image", rect)
                # if cv2.waitKey(0) & 0xff ==27:
                #     cv2.destroyAllWindows()

    def run(self):
        # 根据操作系统路径前缀和年月日以及试卷id生成试卷电子化保存的路径
        today = datetime.date.today()
        if platform_os_type.lower().index('windows') >= 0:
            store_path = windows_store_prefix + str(today.year) + os.sep + str(today.month) + os.sep + str(today.day) + os.sep
        elif platform_os_type.lower().index('linux') >= 0:
            store_path = linux_store_prefix + str(today.year) + os.sep + str(today.month) + os.sep + str(today.day) + os.sep

        # 判断目录是否存在, 不存在则创建.
        is_exists = os.path.exists(store_path)
        if not is_exists:
            os.makedirs(store_path)

        file_type = filetype.guess(self.sheet_file)
        if filetype is None:
            print("Cannot guess file type!")

        # 如果扫描文件是pdf格式的, 则需要先转换为图像.
        img_path = self.sheet_file
        if file_type.extension == 'pdf':
            img_path = self._convert_pdf2img(self.sheet_file, store_path)

        # 判断图片是否需要旋转

        # 对扫描图像进行噪声处理

        # 对扫描图像进行信息提取
        self._extract_shape(img_path)

        # 将图像重新命名为考生编号
