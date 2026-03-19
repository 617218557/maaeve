import time

from PySide6.QtCore import QThread, Signal
from maa.resource import Resource
from maa.context import Context, Tasker

from maa.toolkit import AdbDevice

from app.script.device_utils import connect_device
from app.script.log import MaaTaskerEventSink, MaaControllerEventSink
from app.script.task_maa import start_maa_task

class DeviceTaskThread(QThread):
    """设备任务线程"""
    finished = Signal(str)  # 任务完成信号
    error = Signal(str)  # 错误信号
    stopped = Signal(str)  # 任务停止信号

    def __init__(self, device: AdbDevice):
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

            # 加载资源
            resource = Resource()
            resource_path = "./assets/resource"
            res_job = resource.post_bundle(resource_path)
            res_job.wait()

            tasker = Tasker()
            tasker.add_sink(MaaTaskerEventSink(self.device))
            tasker.add_sink(MaaControllerEventSink(self.device))
            tasker.bind(resource, controller)

            while not self._is_stopped:
                start_maa_task(controller, tasker)
                time.sleep(2)

            self.stopped.emit(f"设备 {self.device.name} 已停止")
        except Exception as e:
            self.error.emit(f"设备 {self.device.name} 异常: {str(e)}")