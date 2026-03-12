from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QVBoxLayout, QLabel, QHBoxLayout, QWidget
from qfluentwidgets import ScrollArea, FluentWidget, PushButton, FluentIcon, TitleLabel, BodyLabel, CardWidget, ListWidget

from app.script.device_utils import find_devices
from app.script.storage import save_device


class HomeInterface(ScrollArea):

    def __init__(self, parent=None):
        super().__init__(parent)
        # 设备列表
        self.device_list = None
        # 添加设备按钮
        self.add_devices_btn = None
        # 选中的item
        self.select_device = None

        self.view = QWidget(self)
        self.parent_layout = QVBoxLayout(self.view)
        self.setWidget(self.view)
        self.setWidgetResizable(True)
        self.parent_layout.setSpacing(20)
        self.parent_layout.setContentsMargins(36, 20, 36, 36)
        self.setObjectName('配置页面')
        self._create_title_section()

    def _create_title_section(self):
        device_layout = QHBoxLayout()
        # 查模拟器
        sync_devices_btn = PushButton(FluentIcon.SYNC, '刷新设备')
        sync_devices_btn.setFixedSize(120, 40)
        sync_devices_btn.clicked.connect(self.on_sync_devices_clicked)
        device_layout.addWidget(sync_devices_btn)

        # 添加模拟器
        self.add_devices_btn = PushButton(FluentIcon.ADD, '添加设备')
        self.add_devices_btn.setFixedSize(120, 40)
        self.add_devices_btn.setEnabled(False)
        self.add_devices_btn.clicked.connect(self.add_device)
        device_layout.addWidget(self.add_devices_btn)
        device_layout.addStretch(1)
        self.parent_layout.addLayout(device_layout)

        # 设备列表
        device_list_card = CardWidget()
        device_list_layout = QVBoxLayout(device_list_card)
        device_list_layout.setContentsMargins(0, 10, 0, 10)
        self.device_list = ListWidget(device_list_card)
        self.device_list.setFixedHeight(300)
        self.device_list.itemClicked.connect(self.on_list_selection_changed)

        device_list_layout.addWidget(self.device_list)
        self.parent_layout.addWidget(device_list_card)

        self.parent_layout.addStretch(1)

    def on_sync_devices_clicked(self):
        devices = find_devices()
        self.device_list.clear()
        self.select_device = None
        self.add_devices_btn.setEnabled(False)
        for device in devices:
            self.device_list.addItem(device.name + '    ' + device.address)
            self.device_list.item(self.device_list.count() - 1).setData(Qt.ItemDataRole.UserRole, device)

    def on_list_selection_changed(self, item):
        selected_device = item.data(Qt.ItemDataRole.UserRole)
        if not selected_device:
            self.add_devices_btn.setEnabled(False)
            return
        self.select_device = selected_device
        self.add_devices_btn.setEnabled(True)

    def add_device(self):
        if not self.select_device:
            return
        print(f"\n执行添加逻辑：")
        print(f"添加设备 - 名称：{self.select_device.name}，地址：{self.select_device.address}")
        # 保存设备到存储
        if save_device(self.select_device):
            print(f"设备保存成功")
        else:
            print(f"设备已存在或保存失败")