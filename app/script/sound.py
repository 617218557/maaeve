import os
import platform

# 获取资源目录
RESOURCE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'assets')
SOUND_DIR = os.path.join(RESOURCE_DIR, 'sound')


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

def play_beep():
    try:
        system = platform.system()
        if system == "Windows":
            import winsound
            winsound.Beep(500, 1000)
        elif system == "Linux":
            import os
            os.system('beep -f 800 -l 500')
        elif system == "Darwin":  # macOS
            import os
            os.system('afplay /System/Library/Sounds/Ping.aiff')
        return True
    except Exception as e:
        print(f"Failed to play beep: {e}")
        return False


def play_warn():
    """播放警告音"""
    # play_sound('warn.mp3')
    play_beep()