from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QDialog, QVBoxLayout, QLabel
from PyQt5.QtWidgets import QHBoxLayout,QVBoxLayout
from PyQt5.QtWidgets import QLineEdit,QTextEdit,QToolTip
from PyQt5.QtWidgets import QTableWidget,QSpacerItem, QSizePolicy
from PyQt5.QtWidgets import QTableWidgetItem,QWhatsThis,QMessageBox
from PyQt5.QtCore import Qt,QEvent
#选择模型类
class choose_page(QWidget):
    def __init__(self, parent =None):
        super().__init__(parent)

        self.setWindowTitle("选择模型")
        self.resize(700,700)
        
        layout = QVBoxLayout(self)

        layout.addLayout(self.init_search())#添加搜索
        layout.addLayout(self.init_table())#添加表格

        layout.addStretch()
    #重写QDialog类的event方法，当点击(?)时触发提示
    # def event(self, event):
    #     if event.type()==QEvent.EnterWhatsThisMode:
    #         QWhatsThis.leaveWhatsThisMode()
    #         QMessageBox.information(self, "Help", "选择一个模型")
    #     return QDialog.event(self,event)

#搜索栏
    def init_search(self):
        #创建水平视图
        seach_layout = QHBoxLayout()

        seach_text_area = QTextEdit()#搜索框
       # seach_text_area.setFixedSize(300,40)
        seach_text_area.setMaximumHeight(40)
        seach_layout.addWidget(seach_text_area)
        
        btn_seach = QPushButton("搜索")
        seach_layout.addWidget(btn_seach)

        btn_download = QPushButton("下载模型")
        seach_layout.addWidget(btn_download)

        return seach_layout
#模型表
    def init_table(self):
        table_layout = QHBoxLayout()
        
        
        table_widget = QTableWidget(10,2)
        table_widget.setColumnWidth(1,700)
        table_widget.setFixedHeight(650)
        action_layout = QVBoxLayout()#左侧按钮竖直布局
        btn_add = QPushButton("确认")
        action_layout.addWidget(btn_add)
        action_layout.addStretch()

        table_layout.addWidget(table_widget)
        table_layout.addLayout(action_layout)

        return table_layout

class home_page(QWidget):
    def __init__(self, parent =None):
        super().__init__(parent)
        self.resize(700,700)
        home_layout = QVBoxLayout(self)#总空间

        #顶部控件
        header_layout = QHBoxLayout()

        btn_1 = QPushButton("1")
        btn_1.setFixedSize(50,100)
        btn_2 = QPushButton("2")
        btn_3 = QPushButton("3")
        btn_4 = QPushButton("4")

        header_layout.addWidget(btn_1)
        header_layout.addWidget(btn_2)
        header_layout.addWidget(btn_3)
        header_layout.addWidget(btn_4)

        #中间文本显示
        text_area = QTextEdit()
        text_area.setReadOnly(True)
        
        #底部对话
        chat_layout = QHBoxLayout()

        chat_area = QTextEdit()
        chat_area.setBaseSize(800,100)
        chat_area.setMaximumHeight(150)
        chat_layout.addWidget(chat_area)


        btn_send = QPushButton("发送")
        btn_send.setFixedSize(175,75)
        chat_layout.addWidget(btn_send)

        home_layout.addLayout(header_layout)
        home_layout.addWidget(text_area)
        home_layout.addLayout(chat_layout)