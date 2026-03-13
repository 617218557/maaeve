import os
from time import sleep

from PyQt6.QtCore import QThread, pyqtSignal

from maa.context import Context
from maa.pipeline import JTemplateMatch, JRecognitionType
from maa.resource import Resource
from maa.tasker import Tasker

from app.script.device_utils import connect_device

# 获取资源目录
RESOURCE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'assets', 'icons')


class DeviceTaskThread(QThread):
    """设备任务线程"""
    finished = pyqtSignal(str)  # 任务完成信号
    error = pyqtSignal(str)  # 错误信号
    stopped = pyqtSignal(str)  # 任务停止信号

    def __init__(self, device):
        super().__init__()
        self.device = device
        self._is_stopped = False

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

def battle(controller):
    """
    执行战斗任务
    :return: True 如果任意一个图片没识别到
    """
    # 截图
    controller.post_screencap().wait()
    screen = controller.cached_image

    if screen is None:
        print("截图失败")
        return True

    # 识别 1.png 和 2.png
    templates = ['1.png', '2.png']

    # for template_name in templates:
    #     template_path = os.path.join(RESOURCE_DIR, template_name)
    #     result = match_template(screen, template_path)
    #
    #     if result is None:
    #         print(f"未识别到: {template_name}")
    #         return True
    #
    #     print(f"识别到: {template_name}, 位置: {result}")
    #     # 识别到了，点击该区域
    #     sleep(1)

    return False