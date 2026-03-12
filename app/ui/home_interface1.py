from PyQt6.QtWidgets import QVBoxLayout, QLabel, QWidget
from qfluentwidgets import ScrollArea, PrimaryPushButton, BodyLabel, CardWidget, TitleLabel


class HomeInterface1(ScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setObjectName("配置")
        self.view = QWidget(self)
        self.setWidget(self.view)
        self.setWidgetResizable(True)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self.view)
        layout.setSpacing(20)
        layout.setContentsMargins(40, 40, 40, 40)

        # 欢迎标题卡片
        welcome_card = CardWidget(self)
        welcome_layout = QVBoxLayout(welcome_card)
        title_label = TitleLabel("欢迎使用 Fluent应用", welcome_card)
        subtitle_label = BodyLabel("这是一个使用PyQt - Fluent - Widgets构建的现代化桌面应用示例。", welcome_card)
        welcome_layout.addWidget(title_label)
        welcome_layout.addWidget(subtitle_label)
        layout.addWidget(welcome_card)

        # 功能按钮区域
        button_card = CardWidget(self)
        button_layout = QVBoxLayout(button_card)
        self.demo_button = PrimaryPushButton('点击演示动画', button_card)
        # self.demo_button.clicked.connect(self.onDemoClicked)
        button_layout.addWidget(self.demo_button)
        layout.addWidget(button_card)

        layout.addStretch(1)