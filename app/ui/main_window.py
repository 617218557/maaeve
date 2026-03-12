from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from qfluentwidgets import FluentWindow, NavigationItemPosition, NavigationWidget
from qfluentwidgets import FluentIcon as FIF
from .home_interface import HomeInterface
from .home_interface1 import HomeInterface1


class MainWindow(FluentWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("eve 自动化")
        self.setWindowIcon(QIcon("assets/icons/app_icon.png"))
        self.resize(1200, 800)

        # 初始化子界面
        self.homeInterface = HomeInterface(self)
        self.homeInterface1 = HomeInterface1(self)

        # 初始化导航栏
        self.init_navigation()

    def init_navigation(self):
        self.addSubInterface(self.homeInterface,FIF.HOME,"配置页面", NavigationItemPosition.TOP)
        self.addSubInterface(self.homeInterface1, FIF.GAME, "首页1", NavigationItemPosition.TOP)

