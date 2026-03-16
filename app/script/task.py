import os
import time

from PyQt6.QtCore import QThread, pyqtSignal

import cv2
import numpy as np
import random

from app.script.device_utils import connect_device

# 获取资源目录
RESOURCE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'assets',
                            'icons')
# 匹配阈值
TEMPLATE_THRESHOLD = 0.9

class DeviceTaskThread(QThread):
    """设备任务线程"""
    finished = pyqtSignal(str)  # 任务完成信号
    error = pyqtSignal(str)  # 错误信号
    stopped = pyqtSignal(str)  # 任务停止信号

    def __init__(self, device):
        super().__init__()
        self.device = device
        self._is_stopped = False

        kernel = np.ones((2, 2), np.uint8)

        img1 = cv2.imread(RESOURCE_DIR + '/1.png')
        img1_grey = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        self.img1_thresh = cv2.threshold(img1_grey, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
        # self.img1_thresh = cv2.dilate(self.img1_thresh, kernel, iterations=1)

        img2 = cv2.imread(RESOURCE_DIR + '/2.png')
        img2_grey = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
        self.img2_thresh = cv2.threshold(img2_grey, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
        # self.img2_thresh = cv2.dilate(self.img2_thresh, kernel, iterations=1)

        img3 = cv2.imread(RESOURCE_DIR + '/3.png')
        img3_grey = cv2.cvtColor(img3, cv2.COLOR_BGR2GRAY)
        self.img3_thresh = cv2.threshold(img3_grey, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
        # self.img3_thresh = cv2.dilate(self.img3_thresh, kernel, iterations=1)

        img_overview = cv2.imread(RESOURCE_DIR + '/overview.png')
        img_overview_grey = cv2.cvtColor(img_overview, cv2.COLOR_BGR2GRAY)
        self.img_overview_thresh = cv2.threshold(img_overview_grey, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
        # self.img_overview_thresh = cv2.dilate(self.img_overview_thresh, kernel, iterations=1)

        img_visitor = cv2.imread(RESOURCE_DIR + '/visitor.png')
        img_visitor_grey = cv2.cvtColor(img_visitor, cv2.COLOR_BGR2GRAY)
        self.img_visitor_thresh = cv2.threshold(img_visitor_grey, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
        # self.img_visitor_thresh = cv2.dilate(self.img_visitor_thresh, kernel, iterations=1)

    def stop(self):
        """停止任务"""
        self._is_stopped = True

    def run(self):
        try:
            # 连接设备
            controller = connect_device(self.device)
            if self._is_stopped:
                self.stopped.emit(f"设备 {self.device.name} 已停止")
                return

            # 无限循环执行战斗任务，直到用户停止
            while not self._is_stopped:
                battle(controller)

            self.stopped.emit(f"设备 {self.device.name} 已停止")
        except Exception as e:
            self.error.emit(f"设备 {self.device.name} 异常: {str(e)}")

def match_template(img_main_thresh, template_thresh):
    """
    模板匹配
    :param img_main_thresh: 预处理后的截图
    :param template_thresh: 预处理后的模板
    :return: 匹配位置 (x, y) 或 None
    """
    if template_thresh is None:
        return None

    result = cv2.matchTemplate(img_main_thresh, template_thresh, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    if max_val >= TEMPLATE_THRESHOLD:
        return max_loc
    return None


def click_at(controller, location):
    """
    点击指定位置
    :param controller: 控制器
    :param location: 位置 (x, y)
    """
    x, y = location
    # 随机偏移，避免点击同一个位置
    offset_x = random.randint(-10, 10)
    offset_y = random.randint(-10, 10)
    controller.post_click(x + offset_x, y + offset_y).wait()

def run_battle_ship(self, controller):
    #导航 左侧导航
    #self.d.click(30 + ran, 200 + ran)
    #右侧军堡
    click_at(controller, (1095, 83))
    time.sleep(1)
    click_at(controller, (831, 91))
    time.sleep(1.5)


def battle(self, controller):
    """
    执行战斗任务
    :return: True 如果任意一个图片没识别到
    """
    # 截图
    img_main = controller.post_screencap().wait()
    img_main_grey = cv2.cvtColor(img_main, cv2.COLOR_BGR2GRAY)
    img_main_thresh = cv2.threshold(img_main_grey, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    res1 = match_template(img_main_thresh, self.img1_thresh)
    res2 = match_template(img_main_thresh, self.img2_thresh)
    res3 = match_template(img_main_thresh, self.img3_thresh)

    print(res1)
    print(res2)
    print(res3)

    # 打开总览
    loc_over_view = match_template(img_main_thresh, self.img_overview_thresh)
    click_at(self, loc_over_view)

    run_battle_ship(self, controller)
    return False
