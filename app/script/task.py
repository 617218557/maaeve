import threading
import time

from PySide6.QtCore import QThread, Signal
from maa.resource import Resource
from maa.context import Context, Tasker

from maa.toolkit import AdbDevice

from app.maascript.AllInOne import AllInOneAction
from app.maascript.OpenOverViewAction import OpenOverViewAction
from app.maascript.RegionMergeRecognition import RegionMergeRecognition
from app.script.device_utils import connect_device
from app.script.task_maa import start_maa_task


class DeviceTaskThread(QThread):
    """设备任务线程"""
    info = Signal(str) # 运行日志
    finished = Signal(str)  # 任务完成信号
    error = Signal(str)  # 错误信号
    stopped = Signal(str)  # 任务停止信号

    def __init__(self, device: AdbDevice):
        super().__init__()
        self.device = device
        self._is_stopped = False
        self.tasker = Tasker()
        self.controller = None
        self.resource = None

    def stop(self):
        """停止任务"""
        self._is_stopped = True
        if self.tasker and self.tasker.running:
            threading.Thread(target=self.tasker.post_stop).start()

    def run(self):
        if self._is_stopped:
            self.stopped.emit(f"{self.device.name} 已停止")
            return
        try:
            if self.resource is None:
                self.info.emit(f"{self.device.name} 加载资源中")
                self.resource = Resource()
                resource_path = "./assets/resource"
                self.resource.register_custom_recognition("RegionMergeRecognition", RegionMergeRecognition())
                self.resource.register_custom_action("OpenOverView", OpenOverViewAction())
                self.resource.register_custom_action("AllInOne", AllInOneAction())
                self.resource.post_bundle(resource_path).wait()

            # 连接设备
            self.info.emit(f"{self.device.name} 连接设备中")
            self.controller = connect_device(self.device)

            if self._is_stopped:
                self.stopped.emit(f"{self.device.name} 已停止")
                return

            self.tasker.bind(self.resource, self.controller)

            self.stopped.emit(f"{self.device.name} 已开始")
            start_maa_task(self.controller, self.tasker)

            self.stopped.emit(f"{self.device.name} 已停止")
        except Exception as e:
            self.error.emit(f"{self.device.name} 异常: {str(e)}")