from dataclasses import dataclass
from maa.toolkit import AdbDevice


@dataclass
class DeviceInfo:
    """设备信息类"""
    adbDevice: AdbDevice
    thread = None
    isStartAi: bool = False
    """ 上一次跑路时间 """
    lastRunTime: int = 0