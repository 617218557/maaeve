from maa.context import Context
from maa.custom_action import CustomAction
import os
import cv2
import time
import logging
import random
from datetime import datetime

from maa.pipeline import JRecognitionType, JOCR

from app.script.device_utils import click_at, click_roi
from app.script.task_old import match_template, img1_grey, img2_grey, img3_grey, is_in_station, \
    run_battle_ship, img_overview_thresh
from app.script.sound import play_warn

logger = logging.getLogger()

# Debug 文件夹路径（项目根目录）
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(os.path.dirname(SCRIPT_DIR))
DEBUG_DIR = os.path.join(PROJECT_DIR, "debug")
os.makedirs(DEBUG_DIR, exist_ok=True)


class AllInOneAction(CustomAction):
    def run(
            self,
            context: Context,
            argv: CustomAction.RunArg,
    ) -> bool:
        controller = context.tasker.controller
        adb_address = controller.info.get("adb_serial")
        # 截图
        img_main = controller.post_screencap().wait().get()
        img_main_grey = cv2.cvtColor(img_main, cv2.COLOR_BGR2GRAY)
        img_main_thresh = cv2.threshold(img_main_grey, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

        if is_in_station(img_main_thresh):
            logger.info(adb_address + "蹲站中")

            logger.info("准备连接 %s，超时时间 %d 秒", "192.168.1.1", 10, quiet=False)
            time.sleep(30)

        # 打开总览
        loc_over_view = match_template(img_main_thresh, img_overview_thresh)
        if loc_over_view is not None and loc_over_view[0] > 1100:
            click_at(controller, loc_over_view)
            time.sleep(2)

        res1 = match_template(img_main_grey, img1_grey)
        res2 = match_template(img_main_grey, img2_grey)
        res3 = match_template(img_main_grey, img3_grey)

        if res1 is None or res2 is None or res3 is None:
            logger.info(adb_address + "跑路")
            play_warn()

            # 右侧军堡
            click_roi(controller, (995, 63, 177, 48))
            time.sleep(1)

            # 识别停靠
            stop_at = context.run_recognition_direct(
                JRecognitionType.OCR,
                JOCR(
                    expected=["停靠"],
                    roi=(728, 28, 233, 318),
                    threshold=0.7
                ),
                img_main
            )
            if stop_at is not None and stop_at.best_result is not None and stop_at.best_result.box is not None:
                box = stop_at.best_result.box
                click_roi(controller, (box.x, box.y, box.w, box.h))
                time.sleep(1.5)
            else:
                click_at(controller, (831, 91))
                time.sleep(1.5)

            time.sleep(2)
        return True


    def saveImage(self, image):
        """保存截图到 debug 文件夹
        文件名格式: 年-月-日_时:分:秒:毫秒_4位随机数.png
        """
        # 生成文件名
        now = datetime.now()
        timestamp = now.strftime("%Y-%m-%d_%H:%M:%S")
        millis = now.strftime("%f")[:3]  # 毫秒前3位
        rand = random.randint(1000, 9999)  # 4位随机数
        filename = f"{timestamp}:{millis}_{rand}.png"

        # 保存路径
        filepath = os.path.join(DEBUG_DIR, filename)
        cv2.imwrite(filepath, image)