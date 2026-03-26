from PySide6.QtGui import QIcon
from qfluentwidgets import FluentWindow, NavigationItemPosition, NavigationWidget
from qfluentwidgets import FluentIcon as FIF

from app.ui.settings_interface import SettingsInterface
from app.ui.sync_device_interface import SyncDeviceInterface
from app.ui.monitor_interface import MonitorInterface



class MainWindow(FluentWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("eve 自动化")
        self.setWindowIcon(QIcon("assets/image/app_icon.png"))
        self.resize(1200, 800)

        # 初始化子界面
        self.syncDeviceInterface = SyncDeviceInterface(self)
        self.monitorInterface = MonitorInterface(self)
        self.settingsInterface = SettingsInterface(self)

        # 初始化导航栏
        self.init_navigation()

    def init_navigation(self):
        self.addSubInterface(self.syncDeviceInterface, FIF.SYNC,"扫描设备", NavigationItemPosition.TOP)
        self.addSubInterface(self.monitorInterface, FIF.PLAY, "开始", NavigationItemPosition.TOP)
        self.addSubInterface(self.settingsInterface, FIF.SETTING, "设置", NavigationItemPosition.BOTTOM)
