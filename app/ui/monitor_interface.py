from PySide6.QtWidgets import QVBoxLayout, QLabel, QHBoxLayout, QWidget
from qfluentwidgets import ScrollArea, FluentWidget, PushButton, FluentIcon, TitleLabel, BodyLabel, CardWidget, ListWidget, isDarkTheme

from app.script.storage import get_devices, delete_device
from app.script.device_utils import find_devices
from app.script.task import DeviceTaskThread


# 监控脚本运行
class MonitorInterface(ScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.device_threads = {}  # {address: thread}
        self.device_buttons = {}  # {address: (start_btn, delete_btn)}
        self.device_list_widget = None

        self.view = QWidget(self)
        self.parent_layout = QVBoxLayout(self.view)
        self.setWidget(self.view)
        self.setWidgetResizable(True)
        self.setStyleSheet("QScrollArea { border: none; background: transparent; }")
        self.viewport().setStyleSheet("background: transparent;")
        self.view.setStyleSheet("background: transparent;")
        self.parent_layout.setSpacing(20)
        self.parent_layout.setContentsMargins(36, 20, 36, 36)
        self.setObjectName('monitorInterface')
        self.create_item_view()

    def create_item_view(self):
        # 刷新按钮
        refresh_btn = PushButton(FluentIcon.SYNC, '刷新设备', self.view)
        refresh_btn.setFixedSize(120, 40)
        refresh_btn.clicked.connect(self.on_refresh_devices)
        self.parent_layout.addWidget(refresh_btn)

        # 设备列表卡片
        device_list_card = CardWidget(self.view)
        device_list_layout = QVBoxLayout(device_list_card)
        device_list_layout.setContentsMargins(0, 10, 0, 10)

        self.device_list_widget = ListWidget(device_list_card)
        self.device_list_widget.setFixedHeight(400)
        device_list_layout.addWidget(self.device_list_widget)

        self.parent_layout.addWidget(device_list_card)
        self.parent_layout.addStretch(1)

        self.on_refresh_devices()

    def on_refresh_devices(self):
        """刷新设备列表"""
        self.device_list_widget.clear()
        self.device_buttons.clear()

        for device in get_devices():
            self.add_device_item(device)

    def add_device_item(self, device):
        """添加设备项"""
        address = device.get('address')
        item_widget = QWidget()
        item_layout = QHBoxLayout(item_widget)
        item_layout.setContentsMargins(10, 5, 10, 5)

        # 设备名称
        name_label = BodyLabel(device.get('name', ''), item_widget)
        name_label.setMinimumWidth(200)
        item_layout.addWidget(name_label)

        # 启动/停止按钮
        start_btn = PushButton(FluentIcon.PLAY, '启动', item_widget)
        start_btn.setFixedSize(80, 32)
        start_btn.clicked.connect(lambda checked, d=device, btn=start_btn: self.on_toggle_device(d, btn))
        item_layout.addWidget(start_btn)

        # 删除按钮
        delete_btn = PushButton(FluentIcon.DELETE, '删除', item_widget)
        delete_btn.setFixedSize(80, 32)
        delete_btn.clicked.connect(lambda: self.on_delete_device(device))
        item_layout.addWidget(delete_btn)

        self.device_buttons[address] = (start_btn, delete_btn)

        self.device_list_widget.addItem('')
        self.device_list_widget.setItemWidget(
            self.device_list_widget.item(self.device_list_widget.count() - 1),
            item_widget
        )

    def on_toggle_device(self, device, button):
        """切换设备启动/停止状态"""
        address = device.get('address')
        start_btn, delete_btn = self.device_buttons.get(address, (button, button))

        # 停止设备
        if address in self.device_threads and self.device_threads[address].isRunning():
            self._stop_thread(address, start_btn, delete_btn, device.get('name'))
            return

        # 启动设备
        target_device = next((d for d in find_devices() if d.address == address), None)
        if not target_device:
            print(f"未找到设备: {device.get('name')}")
            return

        thread = DeviceTaskThread(target_device)
        thread.finished.connect(lambda msg, addr=address: self._on_task_callback(addr, msg))
        thread.error.connect(lambda msg, addr=address: self._on_task_callback(addr, msg))
        thread.stopped.connect(lambda msg, addr=address: self._on_task_callback(addr, msg))

        self.device_threads[address] = thread
        thread.start()

        # 更新按钮状态
        button.setText('停止')
        button.setIcon(FluentIcon.CLOSE)
        delete_btn.setEnabled(False)

        print(f"正在启动设备: {device.get('name')} - {address}")

    def _on_task_callback(self, address, message):
        """任务回调处理"""
        print(message)
        if address not in self.device_buttons:
            return
        start_btn, delete_btn = self.device_buttons[address]
        self._reset_buttons(start_btn, delete_btn)
        if address in self.device_threads:
            del self.device_threads[address]

    def _stop_thread(self, address, start_btn, delete_btn, device_name):
        """停止线程"""
        thread = self.device_threads.get(address)
        if thread:
            thread.stop()
            if not thread.wait(300):
                thread.terminate()
                thread.wait()
            if address in self.device_threads:
                del self.device_threads[address]
        self._reset_buttons(start_btn, delete_btn)
        print(f"设备 {device_name} 已停止")

    def _reset_buttons(self, start_btn, delete_btn):
        """重置按钮状态"""
        if start_btn:
            start_btn.setText('启动')
            start_btn.setIcon(FluentIcon.PLAY)
        if delete_btn:
            delete_btn.setEnabled(True)

    def on_delete_device(self, device):
        """删除设备"""
        address = device.get('address')
        start_btn, delete_btn = self.device_buttons.get(address, (None, None))

        # 如果设备正在运行，先停止
        if address in self.device_threads and self.device_threads[address].isRunning():
            self._stop_thread(address, start_btn, delete_btn, device.get('name'))

        if delete_device(address):
            print(f"删除设备成功: {device.get('name')}")
            self.on_refresh_devices()
        else:
            print(f"删除设备失败: {device.get('name')}")
