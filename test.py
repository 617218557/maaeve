# python -m pip install maafw
from maa.event_sink import EventSink
from maa.tasker import Tasker
from maa.toolkit import Toolkit
from maa.context import Context, ContextEventSink
from maa.resource import Resource
from maa.controller import (
    AdbController,
    Win32Controller,
    MaaWin32ScreencapMethodEnum,
    MaaWin32InputMethodEnum,
)
from maa.custom_action import CustomAction
from maa.custom_recognition import CustomRecognition


# for register decorator
resource = Resource()


def main():
    user_path = "./"
    Toolkit.init_option(user_path)

    ### For ADB controller ###

    # If not found, try running as administrator
    adb_devices = Toolkit.find_adb_devices()
    if not adb_devices:
        print("No ADB device found.")
        exit()

    # for demo, we just use the first device
    device = adb_devices[0]
    print(device)
    controller = AdbController(
        adb_path=device.adb_path,
        address=device.address,
        screencap_methods=device.screencap_methods,
        input_methods=device.input_methods,
        config=device.config,
    )



if __name__ == "__main__":
    main()