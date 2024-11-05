from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QDialog, QVBoxLayout, QLabel
from PyQt5.QtWidgets import QHBoxLayout,QVBoxLayout,QStackedWidget
from PyQt5.QtWidgets import QLineEdit,QTextEdit,QToolTip,QRadioButton
from PyQt5.QtWidgets import QTableWidget,QSpacerItem, QSizePolicy
from PyQt5.QtWidgets import QTableWidgetItem,QWhatsThis,QMessageBox
from PyQt5.QtCore import Qt,QEvent

Width = [200,400,150,200,100,80]
Tags = ["模型名","说明","参数","主页","文件大小","是否下载","类型"]



#选择模型类
class choose_page(QWidget):
    def __init__(self, parent =None):
        super().__init__(parent)

        self.setWindowTitle("选择模型")
        self.resize(700,700)
        
        layout = QVBoxLayout(self)


        layout.addLayout(self.init_act())

        layout.addLayout(self.init_modle())#添加搜索

        self.table_stack = QStackedWidget()

        self.table_stack.addWidget(self.init_table_tools())#创建tools界面
        self.table_stack.addWidget(self.init_table_vision())#创建vision界面
        self.table_stack.addWidget(self.init_table_more())#更多模型

        layout.addWidget(self.table_stack)
       
    #重写QDialog类的event方法，当点击(?)时触发提示
    # def event(self, event):
    #     if event.type()==QEvent.EnterWhatsThisMode:
    #         QWhatsThis.leaveWhatsThisMode()
    #         QMessageBox.information(self, "Help", "选择一个模型")
    #     return QDialog.event(self,event)

    def init_act(self):

        act_layout = QHBoxLayout()

        lable = QLabel("下载选择")
        lable.setFixedHeight(100)

        btn_reset = QPushButton("刷新")
        btn_reset.setFixedHeight(100)
        act_layout.addWidget(lable)
        act_layout.addStretch()
        act_layout.addWidget(btn_reset)
        return act_layout

#模型类型
    def init_modle(self,):
        modle_layout = QHBoxLayout()

        btn_tool = QPushButton("Tools")
        btn_tool.setFixedHeight(100)
        btn_tool.clicked.connect(lambda : self.table_stack.setCurrentIndex(0))


        btn_vision = QPushButton("Vision")
        btn_vision.setFixedHeight(100)
        btn_vision.clicked.connect(lambda : self.table_stack.setCurrentIndex(1))

        btn_more = QPushButton("More")
        btn_more.setFixedHeight(100)
        btn_more.clicked.connect(lambda : self.table_stack.setCurrentIndex(2))

        modle_layout.addWidget(btn_tool)
        modle_layout.addWidget(btn_vision)
        modle_layout.addWidget(btn_more)
        return modle_layout

       
#模型表
    def init_table_tools(self):

        tools_widget = QWidget()

        widget_layout = QVBoxLayout()

        
        #创建水平视图#搜索栏
        seach_layout = QHBoxLayout()
        seach_text_area = QTextEdit()#搜索框
       # seach_text_area.setFixedSize(300,40)
        seach_text_area.setPlaceholderText("搜索模型...")

        seach_text_area.setMaximumHeight(40)
        seach_layout.addWidget(seach_text_area)
        
        btn_seach = QRadioButton("已下载")
        btn_add= QPushButton("确认")
        seach_layout.addWidget(btn_seach)
        seach_layout.addWidget(btn_add)

        widget_layout.addLayout(seach_layout)
        #表格组件
        table_widget = QTableWidget(10,7)
        for i,width in enumerate(Width):
            table_widget.setColumnWidth(i,width)
       # table_widget.setFixedHeight(650)
        table_widget.setHorizontalHeaderLabels(Tags[:-1])


        widget_layout.addWidget(table_widget)
       
        tools_widget.setLayout(widget_layout)

        return tools_widget

    def init_table_vision(self):

        vision_widget = QWidget()

        widget_layout = QVBoxLayout()

        
        #创建水平视图#搜索栏
        seach_layout = QHBoxLayout()
        seach_text_area = QTextEdit()#搜索框
       # seach_text_area.setFixedSize(300,40)
        seach_text_area.setMaximumHeight(40)
        seach_text_area.setPlaceholderText("搜索模型...")

        seach_layout.addWidget(seach_text_area)
        
        btn_seach = QRadioButton("已下载")
        btn_add= QPushButton("确认")
        seach_layout.addWidget(btn_seach)
        seach_layout.addWidget(btn_add)

        widget_layout.addLayout(seach_layout)
        #表格组件
        table_widget = QTableWidget(10,7)
        for i,width in enumerate(Width):
            table_widget.setColumnWidth(i,width)
       # table_widget.setFixedHeight(650)
        table_widget.setHorizontalHeaderLabels(Tags[:-1])

        #table_widget.setFixedHeight(650)
        widget_layout.addWidget(table_widget)
       
        vision_widget.setLayout(widget_layout)

        return vision_widget
    
    def init_table_more(self):

        more_widget = QWidget()

        widget_layout = QVBoxLayout()

        
        #创建水平视图#搜索栏
        seach_layout = QHBoxLayout()
        seach_text_area = QTextEdit()#搜索框
        seach_text_area.setPlaceholderText("搜索模型...")
       # seach_text_area.setFixedSize(300,40)
        seach_text_area.setMaximumHeight(40)
        seach_layout.addWidget(seach_text_area)
        
        btn_seach = QRadioButton("已下载")
        btn_add= QPushButton("确认")
        seach_layout.addWidget(btn_seach)
        seach_layout.addWidget(btn_add)

        widget_layout.addLayout(seach_layout)
        #表格组件
        table_widget = QTableWidget(10,7)
        for i,width in enumerate(Width):
            table_widget.setColumnWidth(i,width)
       # table_widget.setFixedHeight(650)
        table_widget.setHorizontalHeaderLabels(Tags[:-1])
        widget_layout.addWidget(table_widget)
       
        more_widget.setLayout(widget_layout)

        return more_widget

#聊天页
class home_page(QWidget):
    def __init__(self, parent =None):
        super().__init__(parent)
        self.resize(1200,900)
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