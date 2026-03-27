from maa.toolkit import Toolkit, AdbDevice
from maa.controller import AdbController
import random
from typing import Optional, List
from datetime import datetime

from app.script.model.device_info import DeviceInfo


class DeviceManager:
    """设备管理器"""

    def __init__(self):
        self._devices: List[DeviceInfo] = []

    def add_device(self, adb_device: AdbDevice):
        """添加设备，如果有相同 address 先停止再替换
        :param adb_device: AdbDevice 实例
        """
        existing = self.get_device(adb_device.address)
        if existing:
            # 停止旧线程
            if existing.thread and existing.thread.isRunning():
                existing.thread.stop()
            # 替换为新的 DeviceInfo
            existing.adbDevice = adb_device
            existing.thread = None
            existing.isStartAi = False
            existing.lastUpdateTime = datetime.now()
        else:
            # 新增
            device_info = DeviceInfo(adbDevice=adb_device)
            self._devices.append(device_info)

    def get_device(self, address: str) -> Optional[DeviceInfo]:
        """获取指定 address 的 DeviceInfo"""
        for device_info in self._devices:
            if device_info.adbDevice.address == address:
                return device_info
        return None

    def get_all_devices(self) -> List[DeviceInfo]:
        """获取所有设备信息"""
        return self._devices

    def remove_device(self, address: str) -> bool:
        """删除指定 address 的设备"""
        for i, device_info in enumerate(self._devices):
            if device_info.adbDevice.address == address:
                self._devices.pop(i)
                return True
        return False

    def remove(self, device_info: DeviceInfo) -> bool:
        """删除指定 DeviceInfo"""
        if device_info in self._devices:
            self._devices.remove(device_info)
            return True
        return False

    def update_timestamp(self, address: str) -> bool:
        """更新指定设备的时间戳
        :param address: 设备地址
        :return: 是否更新成功
        """
        device_info = self.get_device(address)
        if device_info:
            device_info.lastUpdateTime = datetime.now()
            return True
        return False


# 全局设备管理器实例
device_manager = DeviceManager()


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
