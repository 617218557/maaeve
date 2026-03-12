# coding:utf-8
import os
from qfluentwidgets import QConfig, ConfigItem, qconfig


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


def get_devices():
    """获取已保存的设备列表"""
    return devicesCfg.get(devicesCfg.devices)


def save_device(device):
    """
    保存设备到配置
    :param device: 设备对象，需要有 name 和 address 属性
    :return: 是否保存成功
    """
    devices = devicesCfg.get(devicesCfg.devices)
    
    # 检查设备是否已存在
    for d in devices:
        if d.get('address') == device.address:
            return False  # 设备已存在
    
    devices.append({
        'name': device.name,
        'address': device.address
    })
    
    devicesCfg.set(devicesCfg.devices, devices)
    devicesCfg.save()  # QConfig.save() 不需要参数，会保存到 load 时指定的文件
    return True


def delete_device(address):
    """
    删除指定地址的设备
    :param address: 设备地址
    :return: 是否删除成功
    """
    devices = devicesCfg.get(devicesCfg.devices)
    new_devices = [d for d in devices if d.get('address') != address]
    
    if len(new_devices) == len(devices):
        return False  # 设备不存在
    
    devicesCfg.set(devicesCfg.devices, new_devices)
    devicesCfg.save()  # QConfig.save() 不需要参数
    return True
