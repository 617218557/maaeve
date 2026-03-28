import traceback

from maa.toolkit import Toolkit
from maa.context import Tasker

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt
import sys
from app.ui.main_window import MainWindow
from qfluentwidgets import setTheme, Theme


def main():
    Toolkit.init_option("./")
    Tasker.set_save_on_error(False)

    # 全局崩溃处理函数
    def handle_crash(exc_type, exc_value, exc_traceback):
        print("程序崩溃啦！")
        traceback.print_exception(exc_type, exc_value, exc_traceback)
    # 安装全局钩子
    sys.excepthook = handle_crash

    # 创建应用实例
    app = QApplication(sys.argv)
    app.setAttribute(Qt.ApplicationAttribute.AA_DontCreateNativeWidgetSiblings)

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