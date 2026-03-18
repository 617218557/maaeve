import os
import time
import platform

from maa.pipeline import JOCR
from maa.toolkit import AdbDevice

from app.script.constants import DEBUG_MODE

# 获取资源目录
RESOURCE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'assets')
SOUND_DIR = os.path.join(RESOURCE_DIR, 'sound')

def log(message: str, device: AdbDevice, is_important=False):
    """统一的日志输出方法
    :param device: 设备信息
    :param message: 日志消息
    :param is_important: 是否为重要日志(即使调试关闭也会显示)
    """
    if DEBUG_MODE or is_important:
         # 获取当前时间戳
        timestamp = time.strftime("%H:%M:%S")
        print(f'[{timestamp}] {device.name}: {message}')


def play_sound(sound_file):
    """
    播放音频文件
    :param sound_file: 音频文件名（位于 assets/sound/ 目录下）
    """
    sound_path = os.path.join(SOUND_DIR, sound_file)
    
    if not os.path.exists(sound_path):
        print(f"音频文件不存在: {sound_path}")
        return
    
    system = platform.system()
    
    try:
        if system == 'Darwin':  # macOS
            os.system(f'afplay "{sound_path}" &')
        elif system == 'Windows':
            os.system(f'powershell -c (New-Object Media.SoundPlayer "{sound_path}").PlaySync()')
        elif system == 'Linux':
            os.system(f'aplay "{sound_path}" &')
        else:
            print(f"不支持的操作系统: {system}")
    except Exception as e:
        print(f"播放音频失败: {e}")


def play_warn():
    """播放警告音"""
    play_sound('warn.mp3')