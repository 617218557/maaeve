import logging
import time
from typing import Optional
from PySide6.QtGui import QTextCursor
from maa.controller import ControllerEventSink, Controller
from maa.event_sink import NotificationType
from maa.tasker import TaskerEventSink, Tasker
from maa.toolkit import AdbDevice
from qfluentwidgets import TextEdit

from app.script.constants import KEY_LOG_MESSAGE, KEY_LOG_ADB_ADDRESS


class MaaControllerEventSink(ControllerEventSink):
    def __init__(self, device: AdbDevice):
        self.device = device

    def on_raw_notification(self, controller: Controller, msg: str, details: dict):
        pass

    def on_controller_action(
            self,
            controller: Controller,
            noti_type: NotificationType,
            detail: ControllerEventSink.ControllerActionDetail,
    ):
        logging.getLogger().info(f"[{self.device.name}] {detail.info}")


class MaaTaskerEventSink(TaskerEventSink):
    def __init__(self, device: AdbDevice):
        self.device = device

    def on_raw_notification(self, tasker: Tasker, msg: str, details: dict):
        pass

    def on_tasker_task(
            self,
            tasker: Tasker,
            noti_type: NotificationType,
            detail: TaskerEventSink.TaskerTaskDetail,
    ):
        logging.getLogger().info(f"[{self.device.name}] {detail.task_id} - {detail.entry}")


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

def create_log_message(adb_address: str, message: str) -> dict:
    """创建日志消息字典
    :param adb_address: 设备地址
    :param message: 日志消息
    :return: 包含 adb_address 和 message 的字典
    """
    return {
        KEY_LOG_ADB_ADDRESS: adb_address,
        KEY_LOG_MESSAGE: message
    }

def get_log_adb_address(message: dict):
    return message[KEY_LOG_ADB_ADDRESS]

def get_log_message(message: dict):
    return message[KEY_LOG_MESSAGE]


def parse_log_message(message_str: str) -> dict:
    """解析日志字符串为字典
    :param message_str: 日志字符串，格式如 "{'adb_address': '127.0.0.1:5555', 'message': '跑路'}"
    :return: 包含 adb_address 和 message 的字典
    """
    import ast
    try:
        return ast.literal_eval(message_str)
    except (ValueError, SyntaxError) as e:
        logging.getLogger().warning(f"解析日志消息失败: {e}")
        return {}