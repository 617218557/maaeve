from dataclasses import dataclass
from typing import Optional, List

from maa.toolkit import AdbDevice

from app.script.task import DeviceTaskThread


@dataclass
class DeviceInfo:
    """设备信息类"""
    adbDevice: AdbDevice
    thread: Optional[DeviceTaskThread] = None
    isStartAi: bool = False


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
                existing.thread.wait(300)
            # 替换为新的 DeviceInfo
            existing.adbDevice = adb_device
            existing.thread = None
            existing.isStartAi = False
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
        """删除指定 address 的设备
        :param address: 设备地址
        :return: 是否删除成功
        """
        for i, device_info in enumerate(self._devices):
            if device_info.adbDevice.address == address:
                self._devices.pop(i)
                return True
        return False

    def remove(self, device_info: DeviceInfo) -> bool:
        """删除指定 DeviceInfo
        :param device_info: DeviceInfo 实例
        :return: 是否删除成功
        """
        if device_info in self._devices:
            self._devices.remove(device_info)
            return True
        return False


# 全局设备管理器实例
device_manager = DeviceManager()