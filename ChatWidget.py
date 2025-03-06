from PyQt5.QtWidgets import  QPushButton, QVBoxLayout, QLabel
from PyQt5.QtWidgets import QHBoxLayout,QVBoxLayout
from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtWidgets import QComboBox

class ChatWidget:
    """底部对话类"""
    def __init__(self, parent):
        self.parent = parent
        
    def init_layout(self):
        chat_layout = QHBoxLayout()
        
        # 创建聊天输入区
        chat_area = QTextEdit()
        chat_area.setPlaceholderText("请输入对话内容")
        chat_area.setFontPointSize(15)
        chat_area.setBaseSize(800,100)
        chat_area.setMaximumHeight(150)
        chat_layout.addWidget(chat_area)
        
        # 创建右侧控件布局
        chat_btn_layout = QVBoxLayout()
        choose_layout = QHBoxLayout()

        btn_choose_file = QPushButton("选择文件")
        self.parent.db_messages = []
        self.parent.file_paths = None

        label = QLabel("模型选择")
        model_path_label = QLabel("未选择文件")
        btn_choose_file.clicked.connect(lambda: self.parent.open_file_dialog(model_path_label))

        cbox_change = QComboBox()
        cbox_change.addItems(self.parent.get_model())
        cbox_change.currentTextChanged.connect(self.parent.on_model_changed)
        
        self.parent.current_model = cbox_change.currentText()

        btn_send = QPushButton("发送")
        btn_send.setFixedSize(175,75)
        btn_send.clicked.connect(lambda: self.parent.send_message(
            chat_area,
            self.parent.current_model,
            self.parent.or_model(self.parent.current_model)
        ))

        # 添加控件到布局
        choose_layout.addWidget(label)
        choose_layout.addWidget(btn_choose_file)

        chat_btn_layout.addLayout(choose_layout)
        chat_btn_layout.addWidget(model_path_label)
        chat_btn_layout.addWidget(cbox_change)
        chat_btn_layout.addWidget(btn_send)

        chat_layout.addLayout(chat_btn_layout)
        
        return chat_layout
