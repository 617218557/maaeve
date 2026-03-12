from PyQt6.QtGui import QIcon
from qfluentwidgets import FluentWindow, NavigationItemPosition, NavigationWidget
from qfluentwidgets import FluentIcon as FIF
from app.ui.home_interface import HomeInterface


class MainWindow(FluentWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("eve 自动化")
        self.setWindowIcon(QIcon("assets/icons/app_icon.png"))
        self.resize(1200, 800)

        # 初始化子界面
        self.homeInterface = HomeInterface(self)

        # 初始化导航栏
        self.init_navigation()

    def init_navigation(self):
        self.addSubInterface(self.homeInterface,FIF.HOME,"配置页面", NavigationItemPosition.TOP)
