import os
import time
import cv2
import numpy as np
import random
from maa.resource import Resource
from maa.context import Context, Tasker

from PyQt6.QtCore import QThread, pyqtSignal
from maa.toolkit import AdbDevice

from app.script.device_utils import connect_device
from app.script.task_maa import start_maa_task

class DeviceTaskThread(QThread):
    """设备任务线程"""
    finished = pyqtSignal(str)  # 任务完成信号
    error = pyqtSignal(str)  # 错误信号
    stopped = pyqtSignal(str)  # 任务停止信号

    def __init__(self, device: AdbDevice):
        super().__init__()
        self.device = device
        self._is_stopped = False

        # 连接设备
        self.controller = connect_device(self.device)
        if self._is_stopped:
            self.stopped.emit(f"设备 {self.device.name} 已停止")
            return

        resource = Resource()
        resource_path = "./assets/resource"
        res_job = resource.post_bundle(resource_path)
        res_job.wait()

        self.tasker = Tasker()
        self.tasker.bind(resource, self.controller)


    def stop(self):
        """停止任务"""
        self._is_stopped = True

    def run(self):
        try:
            while not self._is_stopped:
                # battle(controller = controller, device = self.device)

                start_maa_task(self.controller, self.tasker)

                time.sleep(2)

            self.stopped.emit(f"设备 {self.device.name} 已停止")
        except Exception as e:
            self.error.emit(f"设备 {self.device.name} 异常: {str(e)}")