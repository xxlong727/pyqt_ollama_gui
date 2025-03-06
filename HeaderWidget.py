from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QHBoxLayout

class HeaderWidget:
    """顶部控件类"""
    def __init__(self, parent):
        self.parent = parent
        
    def init_layout(self):
        header_layout = QHBoxLayout()
        
        btn_new = QPushButton("新建对话") 
        btn_store = QPushButton("保存对话")
        btn_load = QPushButton("历史加载")

        btn_new.setFixedHeight(100)
        btn_store.setFixedHeight(100)
        btn_load.setFixedHeight(100)

        btn_new.clicked.connect(lambda: self.parent.reset_chat())
        btn_store.clicked.connect(lambda: self.parent.message_to_db())
        btn_load.clicked.connect(lambda: self.parent.load_message())

        header_layout.addWidget(btn_new)
        header_layout.addWidget(btn_store)
        header_layout.addWidget(btn_load)
        
        return header_layout