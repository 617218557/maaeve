# coding:utf-8
import os
from qfluentwidgets import QConfig, ConfigItem, qconfig

from maa.toolkit import AdbDevice


# 配置文件路径
CONFIG_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'config')
DEVICES_FILE = os.path.join(CONFIG_DIR, 'devices.json')

# 确保配置目录存在
os.makedirs(CONFIG_DIR, exist_ok=True)


class DevicesStorage(QConfig):
    """应用配置类"""

    # 设备列表配置项
    devices = ConfigItem("Devices", "SavedDevices", [])


# 设备实例
devicesCfg = DevicesStorage()

# 加载配置文件
qconfig.load(DEVICES_FILE, devicesCfg)


def get_devices() -> list[AdbDevice]:
    """获取已保存的设备列表"""
    devices_data = devicesCfg.get(devicesCfg.devices)
    result = []
    for d in devices_data:
        result.append(AdbDevice(
            name=d.get('name', ''),
            adb_path=d.get('adb_path'),
            address=d.get('address', ''),
            screencap_methods=d.get('screencap_methods', 0),
            input_methods=d.get('input_methods', 0),
            config=d.get('config', {})
        ))
    return result


def save_device(device: AdbDevice) -> bool:
    """
    保存设备到配置
    :param device: AdbDevice 对象
    :return: 是否保存成功
    """
    devices = devicesCfg.get(devicesCfg.devices)
    
    # 检查设备是否已存在
    for d in devices:
        if d.get('address') == device.address:
            return False  # 设备已存在
    
    # 保存设备信息
    device_data = {
        'name': device.name,
        'address': device.address,
        'adb_path': str(device.adb_path) if device.adb_path else None,
        'screencap_methods': device.screencap_methods,
        'input_methods': device.input_methods,
        'config': device.config
    }
    
    devices.append(device_data)
    
    devicesCfg.set(devicesCfg.devices, devices)
    devicesCfg.save()
    return True


def delete_device(device: AdbDevice) -> bool:
    """
    删除指定设备
    :param device: AdbDevice 对象
    :return: 是否删除成功
    """
    devices = devicesCfg.get(devicesCfg.devices)
    new_devices = [d for d in devices if d.get('address') != device.address]
    
    if len(new_devices) == len(devices):
        return False  # 设备不存在
    
    devicesCfg.set(devicesCfg.devices, new_devices)
    devicesCfg.save()
    return True
