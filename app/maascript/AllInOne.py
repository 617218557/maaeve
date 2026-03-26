from maa.context import Context
from maa.custom_action import CustomAction
import cv2
import time
import logging

from maa.pipeline import JRecognitionType, JOCR

from app.script.device_utils import click_at, click_roi
from app.script.log import create_log_message
from app.script.storage import settingsCfg, saveImage
from app.script.task_old import match_template, img1_grey, img2_grey, img3_grey, is_in_station, \
    run_battle_ship, img_overview_thresh
from app.script.sound import play_warn

logger = logging.getLogger()

class AllInOneAction(CustomAction):
    def run(
            self,
            context: Context,
            argv: CustomAction.RunArg,
    ) -> bool:
        controller = context.tasker.controller
        adb_address = controller.info.get("adb_serial")
        if adb_address is None:
            adb_address = ""
        # 截图
        img_main = controller.post_screencap().wait().get()
        img_main_grey = cv2.cvtColor(img_main, cv2.COLOR_BGR2GRAY)
        img_main_thresh = cv2.threshold(img_main_grey, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
        if is_in_station(img_main_thresh):
            logger.info(create_log_message(adb_address, "蹲站中"))
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
            logger.info(create_log_message(adb_address, "跑路"))
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
                    threshold=settingsCfg.get(settingsCfg.threshold)
                ),
                img_main
            )
            if stop_at is not None and stop_at.best_result is not None and stop_at.best_result.box is not None:
                box = stop_at.best_result.box
                click_roi(controller, (box.x, box.y, box.w, box.h))
            else:
                click_at(controller, (831, 91))
            if settingsCfg.get(settingsCfg.saveScreenshot):
                saveImage(img_main)
            time.sleep(1.5)
        return True