from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel
from PyQt5.QtWidgets import QHBoxLayout,QVBoxLayout
from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtWidgets import QComboBox
import ollama

class home_page(QWidget):
    def __init__(self, parent =None):
        super().__init__(parent)
        self.resize(1200,900)
        home_layout = QVBoxLayout(self)#总空间
        #加载组件
        home_layout.addLayout(self.init_head())
        home_layout.addWidget(self.init_show())
        home_layout.addLayout(self.init_chat())
    #顶部控件
    def init_head(self):
        header_layout = QHBoxLayout()

        btn_new = QPushButton("新建对话")
        #btn_change = QPushButton("切换模型")
        btn_store = QPushButton("保存对话")
        btn_load = QPushButton("历史加载")

        btn_new.setFixedHeight(100)
        #btn_change.setFixedHeight(100)
        btn_store.setFixedHeight(100)
        btn_load.setFixedHeight(100)


        header_layout.addWidget(btn_new)
        #header_layout.addWidget(btn_change)
        header_layout.addWidget(btn_store)
        header_layout.addWidget(btn_load)
        return header_layout
    #中间文本显示   
    def init_show(self):
        
        text_area = QTextEdit()
        text_area.setReadOnly(True)
        return text_area
    #底部对话
    def init_chat(self):
        chat_layout = QHBoxLayout()

        chat_area = QTextEdit()
        chat_area.setBaseSize(800,100)
        chat_area.setMaximumHeight(150)
        chat_layout.addWidget(chat_area)

        
        chat_btn_laout = QVBoxLayout() #右侧的三个排布

        label = QLabel("模型选择")#创建标签
        cbox_change = QComboBox()# 创建下拉框

        cbox_change.addItems(self.get_model())

        #cbox_change.addItem("切换模型")
        btn_send = QPushButton("发送")
        btn_send.setFixedSize(175,75)
        #btn_change.setFixedSize(175,75)

        chat_btn_laout.addWidget(label)
        chat_btn_laout.addWidget(cbox_change)
        chat_btn_laout.addWidget(btn_send)

        chat_layout.addLayout(chat_btn_laout)

        
        return chat_layout
    
    def get_model(self):
        from ollama import ListResponse
        ollama_model_list:ListResponse = ollama.list()

        model_list = [model.model for model in ollama_model_list.models]
        return model_list