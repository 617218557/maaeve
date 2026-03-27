from PySide6.QtCore import Qt
from PySide6.QtWidgets import QVBoxLayout, QLabel, QHBoxLayout, QWidget
from qfluentwidgets import ScrollArea, FluentWidget, PushButton, FluentIcon, TitleLabel, BodyLabel, CardWidget, \
    ListWidget, isDarkTheme, LineEdit, SwitchButton, SwitchSettingCard, RangeSettingCard, PushSettingCard

from app.script.storage import save_device, settingsCfg, clear_screenshots


# 设置
class SettingsInterface(ScrollArea):

    def __init__(self, parent=None):
        super().__init__(parent)
        # 设备列表
        self.device_list = None
        # 添加设备按钮
        self.add_devices_btn = None
        # 选中的item
        self.select_device = None

        # 匹配阈值输入框
        self.threshold_input = None
        # 跑路保存截图开关
        self.save_screenshot_switch = None
        # 自动出站开关
        self.auto_exit_switch = None

        self.view = QWidget(self)
        self.parent_layout = QVBoxLayout(self.view)
        self.setWidget(self.view)
        self.setWidgetResizable(True)
        # 设置透明背景
        self.setStyleSheet("QScrollArea { border: none; background: transparent; }")
        self.viewport().setStyleSheet("background: transparent;")
        self.view.setStyleSheet("background: transparent;")
        self.parent_layout.setSpacing(20)
        self.parent_layout.setContentsMargins(36, 20, 36, 36)
        self.setObjectName('设置')
        self.create_item_view()

    def create_item_view(self):
        threshold_card = RangeSettingCard(
            settingsCfg.threshold,
            FluentIcon.EDIT,
            title="匹配阈值",
            content=""
        )
        self.parent_layout.addWidget(threshold_card)

        save_screenshot_card = SwitchSettingCard(
            icon = FluentIcon.SAVE,
            title = "跑路保存截图",
            content = "",
            configItem = settingsCfg.saveScreenshot
        )
        self.parent_layout.addWidget(save_screenshot_card)

        auto_battle_card = SwitchSettingCard(
            icon=FluentIcon.PLAY,
            title="自动出站",
            content="占位 还没实现",
            configItem=settingsCfg.autoStartAi
        )
        self.parent_layout.addWidget(auto_battle_card)

        clear_cache_card = PushSettingCard(
            text="清理缓存",
            icon=FluentIcon.DELETE,
            title="清理缓存",
            content="一键删除截图文件"
        )
        clear_cache_card.clicked.connect(self.clearCache)
        self.parent_layout.addWidget(clear_cache_card)


        self.parent_layout.addStretch(1)

    def clearCache(self):
        clear_screenshots()
