import logging
import time
from typing import Optional
from PySide6.QtGui import QTextCursor
from PySide6.QtCore import QObject, Signal
from maa.toolkit import AdbDevice
from qfluentwidgets import TextEdit


# 日志转发器 - 用于跨线程日志传递
class LogForwarder(QObject):
    log_signal = Signal(str, str)  # (message, level)

    def __init__(self, parent=None):
        super().__init__(parent)


class QtLogHandler(logging.Handler):
    """自定义日志处理器，将日志发送到 PyQt 信号"""

    def __init__(self, callback):
        super().__init__()
        self.callback = callback  # 回调函数，用于在主线程中显示日志

    def emit(self, record):
        try:
            msg = self.format(record)
            level = record.levelname
            # 将日志消息通过回调函数传递
            self.callback(msg, level)
        except Exception:
            self.handleError(record)


def append_colored_log(log_view: TextEdit, text: str, level: str, device: Optional[AdbDevice] = None):
    """将带颜色的日志输出到 QTextEdit
    :param log_view: QTextEdit 控件
    :param text: 日志文本
    :param level: 日志级别 (INFO/SYSTEM/ERROR/WARN)
    :param device: 设备对象（可选）
    """
    if not log_view:
        return
    # 时间戳
    now = time.strftime("%H:%M:%S")
    # 添加设备名称
    device_name = f" [{device.name}]" if device else ""
    log_str = f"[{now}]{device_name} {text}"

    # 颜色配置
    color_map = {
        "INFO": "#A6E3A1",  # 绿
        "SYSTEM": "#89B4FA",  # 蓝
        "ERROR": "#F38BA8",  # 红
        "WARN": "#F9C267"  # 黄
    }
    color = color_map.get(level, "#FFFFFF")

    # 富文本插入
    log_view.append(f'<span style="color:{color};">{log_str}</span>')

    # 自动滚动到底部
    cursor = log_view.textCursor()
    cursor.movePosition(QTextCursor.MoveOperation.End)
    log_view.setTextCursor(cursor)