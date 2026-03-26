import logging
import os
import cv2
import time
import random
import numpy as np
from maa.toolkit import AdbDevice

from app.script.device_utils import click_at, click_roi
from app.script.sound import play_warn
from app.script.storage import settingsCfg

logger = logging.getLogger()
# 获取资源目录
RESOURCE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'assets', 'resource','image')

kernel = np.ones((2, 2), np.uint8)
img1 = cv2.imread(RESOURCE_DIR + '/1.png')
img1_grey = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
# img1_thresh = cv2.threshold(img1_grey, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
# self.img1_thresh = cv2.dilate(self.img1_thresh, kernel, iterations=1)

img2 = cv2.imread(RESOURCE_DIR + '/2.png')
img2_grey = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
# img2_thresh = cv2.threshold(img2_grey, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
# self.img2_thresh = cv2.dilate(self.img2_thresh, kernel, iterations=1)

img3 = cv2.imread(RESOURCE_DIR + '/3.png')
img3_grey = cv2.cvtColor(img3, cv2.COLOR_BGR2GRAY)
# img3_thresh = cv2.threshold(img3_grey, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
# self.img3_thresh = cv2.dilate(self.img3_thresh, kernel, iterations=1)

img_overview = cv2.imread(RESOURCE_DIR + '/overview.png')
img_overview_grey = cv2.cvtColor(img_overview, cv2.COLOR_BGR2GRAY)
img_overview_thresh = cv2.threshold(img_overview_grey, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
# self.img_overview_thresh = cv2.dilate(self.img_overview_thresh, kernel, iterations=1)

img_visitor = cv2.imread(RESOURCE_DIR + '/visitor.png')
img_visitor_grey = cv2.cvtColor(img_visitor, cv2.COLOR_BGR2GRAY)
img_visitor_thresh = cv2.threshold(img_visitor_grey, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
# self.img_visitor_thresh = cv2.dilate(self.img_visitor_thresh, kernel, iterations=1)


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

    if max_val >= settingsCfg.get(settingsCfg.threshold):
        return max_loc
    return None

def run_battle_ship(controller):
    #导航 左侧导航
    #self.d.click(30 + ran, 200 + ran)
    #右侧军堡
    click_roi(controller, (995, 63, 177, 48))
    time.sleep(1)
    click_roi(controller, (754, 152, 91, 10))
    time.sleep(1.5)


def is_in_station(img_main):
    """检测是否在空间站内"""
    result = match_template(img_main, img_visitor_thresh)
    if result is not None:
        return True
    return False

def battle(controller, device: AdbDevice):
    """
    执行战斗任务
    :return: True 如果任意一个图片没识别到
    """
    # 截图
    img_main = controller.post_screencap().wait().get()
    img_main_grey = cv2.cvtColor(img_main, cv2.COLOR_BGR2GRAY)
    img_main_thresh = cv2.threshold(img_main_grey, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    if is_in_station(img_main_thresh):
        logger.info(device.name + ": 蹲站中")
        time.sleep(30)
        return False

    # 打开总览
    loc_over_view = match_template(img_main_thresh, img_overview_thresh)
    if loc_over_view is not None and loc_over_view[0] > 1100:
        click_at(controller, loc_over_view)
        time.sleep(2)

    res1 = match_template(img_main_grey, img1_grey)
    res2 = match_template(img_main_grey, img2_grey)
    res3 = match_template(img_main_grey, img3_grey)
    # res4 = match_template(img_main_thresh, img_overview_thresh)
    # res5 = match_template(img_main_thresh, img_visitor_thresh)

    if res1 is None or res2 is None or res3 is None:
        logger.info(device.name + ": 跑路")
        play_warn()
        run_battle_ship(controller)
        time.sleep(3)
        return True

    return False