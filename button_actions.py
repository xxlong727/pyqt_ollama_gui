from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QDialog, QVBoxLayout, QLabel
from PyQt5.QtWidgets import QHBoxLayout,QVBoxLayout,QStackedWidget
from PyQt5.QtWidgets import QLineEdit,QTextEdit,QToolTip,QRadioButton
from PyQt5.QtWidgets import QTableWidget,QSpacerItem, QSizePolicy
from PyQt5.QtWidgets import QTableWidgetItem,QComboBox
from PyQt5.QtCore import Qt,QEvent

import pymysql

Width = [200,400,150,200,100,80]
Tags = ["模型名","说明","参数-大小","主页","是否下载","类型"]



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

#模型类型页
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

       
#模型tools表
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
        table_widget.setHorizontalHeaderLabels(Tags[:-1])#去掉最后一列

        connect = pymysql.connect(host='localhost',
                                  user='root',
                                  password='xxlong727',
                                  database='model_ollama',
                                  charset='utf8mb4')
        with connect.cursor() as cursor:
            
            try:
                query = """
                        SELECT model.model_id, model.name, model.description, model.home, model.isdownloaded, model.type,
                            parameters.para_id,parameters.size_storage
                        FROM model
                        JOIN parameters ON model.model_id = parameters.model_id
                        WHERE model.type = 'tools';
                        """
                cursor.execute(query)
                data = cursor.fetchall()
                #print(1111111111111111111111)
                #print(data)
                row = 0
                for model_data in data:
                    table_widget.setItem(row, 0, QTableWidgetItem(model_data[1]))
                    table_widget.setItem(row, 1, QTableWidgetItem(model_data[2]))
                    table_widget.setItem(row, 2, QTableWidgetItem(model_data[7]))
                    table_widget.setItem(row, 3, QTableWidgetItem(model_data[3]))
                    table_widget.setItem(row, 4, QTableWidgetItem(str(model_data[4])))
                    table_widget.setItem(row, 5, QTableWidgetItem(model_data[4]))
                    # 为参数大小列添加QComboBox
                    
                    row += 1
            except pymysql.MySQLError as e:
                print(f"Error fetching data: {e}")

        widget_layout.addWidget(table_widget) 
       
        tools_widget.setLayout(widget_layout)

        return tools_widget
#视觉模型
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
        table_widget.setHorizontalHeaderLabels(Tags[:-1])#去掉最后一列 
        connect = pymysql.connect(host='localhost',
                                  user='root',
                                  password='xxlong727',
                                  database='model_ollama',
                                  charset='utf8mb4')
        with connect.cursor() as cursor:
            
            try:
                query = """
                        SELECT model.model_id, model.name, model.description, model.home, model.isdownloaded, model.type,
                            parameters.para_id,parameters.size_storage
                        FROM model
                        JOIN parameters ON model.model_id = parameters.model_id
                        WHERE model.type = 'vision';
                        """
                cursor.execute(query)
                data = cursor.fetchall()
                #print(1111111111111111111111)
                #print(data)
                row = 0
                for model_data in data:
                    table_widget.setItem(row, 0, QTableWidgetItem(model_data[1]))
                    table_widget.setItem(row, 1, QTableWidgetItem(model_data[2]))
                    table_widget.setItem(row, 2, QTableWidgetItem(model_data[7]))
                    table_widget.setItem(row, 3, QTableWidgetItem(model_data[3]))
                    table_widget.setItem(row, 4, QTableWidgetItem(str(model_data[4])))
                    table_widget.setItem(row, 5, QTableWidgetItem(model_data[4]))
                    # 为参数大小列添加QComboBox
                    
                    row += 1
            except pymysql.MySQLError as e:
                print(f"Error fetching data: {e}")
        #table_widget.setFixedHeight(650)
        widget_layout.addWidget(table_widget)
       
        vision_widget.setLayout(widget_layout)

        return vision_widget
#更多模型  
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
        connect = pymysql.connect(host='localhost',
                                  user='root',
                                  password='xxlong727',
                                  database='model_ollama',
                                  charset='utf8mb4')
        with connect.cursor() as cursor:
            
            try:
                query = """
                        SELECT model.model_id, model.name, model.description, model.home, model.isdownloaded, model.type,
                            parameters.para_id,parameters.size_storage
                        FROM model
                        JOIN parameters ON model.model_id = parameters.model_id
                        WHERE model.type = 'more';
                        """
                cursor.execute(query)
                data = cursor.fetchall()
                #print(1111111111111111111111)
                #print(data)
                row = 0
                for model_data in data:
                    table_widget.setItem(row, 0, QTableWidgetItem(model_data[1]))
                    table_widget.setItem(row, 1, QTableWidgetItem(model_data[2]))
                    table_widget.setItem(row, 2, QTableWidgetItem(model_data[7]))
                    table_widget.setItem(row, 3, QTableWidgetItem(model_data[3]))
                    table_widget.setItem(row, 4, QTableWidgetItem(str(model_data[4])))
                    table_widget.setItem(row, 5, QTableWidgetItem(model_data[4]))
                    # 为参数大小列添加QComboBox
                    
                    row += 1
            except pymysql.MySQLError as e:
                print(f"Error fetching data: {e}")
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