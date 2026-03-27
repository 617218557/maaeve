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
    :param roi: 区域坐标 (x起始坐标, y起始坐标, x偏移, y偏移)
    """
    x, y, offset_x, offset_y = roi
    # 计算实际坐标
    click_x = x + random.randint(0, offset_x)
    click_y = y + random.randint(0, offset_y)
    # 执行点击
    controller.post_click(click_x, click_y).wait()


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
