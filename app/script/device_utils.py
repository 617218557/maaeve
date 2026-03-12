from maa.toolkit import Toolkit


def find_devices():
    adb_devices = Toolkit.find_adb_devices()
    return adb_devices