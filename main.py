from maa.toolkit import Toolkit

from PySide6.QtWidgets import (
    QApplication,
)
import sys
from app.ui.main_window import MainWindow
from qfluentwidgets import setTheme, Theme


def main():
    Toolkit.init_option("./")
    # 创建应用实例
    app = QApplication(sys.argv)
    app.setApplicationName("mma eve")
    app.setApplicationVersion("1.0.0")
    setTheme(Theme.DARK)

    # 创建并显示主窗口
    window = MainWindow()
    window.show()

    # 运行应用
    app.exec()

if __name__ == "__main__":
    main()