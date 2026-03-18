from maa.toolkit import Toolkit, AdbDevice
from maa.controller import AdbController
import random

def find_devices():
    adb_devices = Toolkit.find_adb_devices()
    return adb_devices


def connect_device(device: AdbDevice):
    """连接设备"""
    controller = AdbController(
        adb_path=device.adb_path,
        address=device.address,
        screencap_methods=device.screencap_methods,
        # screencap_methods=MaaAdbScreencapMethodEnum.EmulatorExtras,
        input_methods=device.input_methods,
        config=device.config,
    )
    controller.post_connection().wait()
    return controller

# 点击区域内任意点
def click_roi(controller, roi):
    """
    点击指定区域内的任意坐标
    :param controller: AdbController 实例
    :param roi: 区域坐标 (x1, y1, x2, y2)
    """
    x1, y1, x2, y2 = roi
    # 在区域内随机生成坐标
    x = random.randint(x1, x2)
    y = random.randint(y1, y2)
    # 执行点击
    controller.post_click(x, y).wait()