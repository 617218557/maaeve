# coding:utf-8
import os
import random
from datetime import datetime

import cv2
from qfluentwidgets import QConfig, ConfigItem, qconfig, BoolValidator, OptionsConfigItem, RangeValidator, \
    RangeConfigItem

from maa.toolkit import AdbDevice


# 配置文件路径
CONFIG_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'config')
CONFIG_DEVICES_FILE = os.path.join(CONFIG_DIR, 'devices.json')
CONFIG_SETTINGS_FILE = os.path.join(CONFIG_DIR, 'settings.json')


# Debug 文件夹路径（项目根目录）
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(os.path.dirname(SCRIPT_DIR))
IMAGE_CACHE_DIR = os.path.join(PROJECT_DIR, "debug", "screenshot")
os.makedirs(IMAGE_CACHE_DIR, exist_ok=True)

# 确保配置目录存在
os.makedirs(CONFIG_DIR, exist_ok=True)


class DevicesStorage(QConfig):
    """应用配置类"""

    # 设备列表配置项
    devices = ConfigItem("Devices", "SavedDevices", [])


class SettingsStorage(QConfig):
    """设置配置类"""

    # 匹配阈值
    threshold = RangeConfigItem("Settings", "Threshold", 80, RangeValidator(60, 100))

    # 跑路保存截图
    saveScreenshot = ConfigItem("Settings", "SaveScreenshot", False)

    # 自动出站
    autoStartAi = ConfigItem("Settings", "AutoStartAi", False)

    # 自动出站随机时间
    autoStartTime = RangeConfigItem("Settings", "AutoStartTime", 10, RangeValidator(6, 60))

# 设备实例
devicesCfg = DevicesStorage()
settingsCfg = SettingsStorage()

# 加载配置文件
qconfig.load(CONFIG_DEVICES_FILE, devicesCfg)
qconfig.load(CONFIG_SETTINGS_FILE, settingsCfg)


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


def saveImage(image):
    """保存截图到 debug 文件夹
    文件名格式: 年-月-日_时:分:秒:毫秒_4位随机数.png
    """
    # 生成文件名
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d_%H:%M:%S")
    millis = now.strftime("%f")[:3]  # 毫秒前3位
    rand = random.randint(1000, 9999)  # 4位随机数
    filename = f"{timestamp}:{millis}_{rand}.png"

    # 保存路径
    filepath = os.path.join(IMAGE_CACHE_DIR, filename)
    cv2.imwrite(filepath, image)


def clear_screenshots():
    """删除 debug/screenshot 目录下所有截图文件"""
    if not os.path.exists(IMAGE_CACHE_DIR):
        return
    for filename in os.listdir(IMAGE_CACHE_DIR):
        if filename.endswith('.png'):
            filepath = os.path.join(IMAGE_CACHE_DIR, filename)
            os.remove(filepath)


def get_threshold() -> float:
    return settingsCfg.get(settingsCfg.threshold) / 100

def get_auto_start_ai() -> bool:
    return settingsCfg.get(settingsCfg.autoStartAi)

def get_auto_start_ai_time() -> int:
    return settingsCfg.get(settingsCfg.autoStartTime) * 60 * 1000