import time

from PySide6.QtCore import QThread, Signal
from maa.resource import Resource
from maa.context import Context, Tasker

from maa.toolkit import AdbDevice

from app.maascript.AllInOne import AllInOneAction
from app.maascript.OpenOverViewAction import OpenOverViewAction
from app.maascript.RegionMergeRecognition import RegionMergeRecognition
from app.script.device_utils import connect_device
from app.script.log import MaaTaskerEventSink, MaaControllerEventSink
from app.script.task_maa import start_maa_task
from app.script.task_old import battle


class DeviceTaskThread(QThread):
    """设备任务线程"""
    finished = Signal(str)  # 任务完成信号
    error = Signal(str)  # 错误信号
    stopped = Signal(str)  # 任务停止信号

    def __init__(self, device: AdbDevice):
        super().__init__()
        self.device = device
        self._is_stopped = False
        self.tasker = Tasker()
        self.controller = None

        # 加载资源
        self.resource = Resource()
        resource_path = "./assets/resource"
        self.resource.register_custom_recognition("RegionMergeRecognition", RegionMergeRecognition())
        self.resource.register_custom_action("OpenOverView", OpenOverViewAction())
        self.resource.register_custom_action("AllInOne", AllInOneAction())
        self.resource.post_bundle(resource_path).wait()


    def stop(self):
        """停止任务"""
        self._is_stopped = True
        self.tasker.post_stop()

    def run(self):
        try:
            # 连接设备
            self.controller = connect_device(self.device)

            # self.tasker.add_sink(MaaTaskerEventSink(self.device))
            # self.tasker.add_sink(MaaControllerEventSink(self.device))
            self.tasker.bind(self.resource, self.controller)
            self.stopped.emit(f"设备 {self.device.name} 已开始")
            start_maa_task(self.controller, self.tasker)

            # while not self._is_stopped:
            #     battle(controller, self.device)

            self.stopped.emit(f"设备 {self.device.name} 已停止")
        except Exception as e:
            self.error.emit(f"设备 {self.device.name} 异常: {str(e)}")