from PyQt5.QtWidgets import  QWidget, QPushButton, QVBoxLayout
from PyQt5.QtWidgets import QHBoxLayout,QVBoxLayout
from PyQt5.QtWidgets import QTextEdit,QRadioButton

class VisionWidget:

    def __init__(self,parent):
        self.parent = parent
    def Init(self):
        vision_widget = QWidget()
        widget_layout = QVBoxLayout()
        
        #创建水平视图#搜索栏
        seach_layout = QHBoxLayout()  
        seach_text_area = QTextEdit()#搜索框
       # seach_text_area.setFixedSize(300,40)
        seach_text_area.setMaximumHeight(40)
        seach_text_area.setPlaceholderText("搜索模型...")

        #seach_text_area.textChanged.connect(self.filter_table)#连接搜索框的信号

        seach_layout.addWidget(seach_text_area)
        
        btn_seach = QRadioButton("已下载")
        btn_add= QPushButton("下载")
        btn_remove = QPushButton("删除")

        seach_layout.addWidget(btn_seach)
        seach_layout.addWidget(btn_add)
        seach_layout.addWidget(btn_remove)

        widget_layout.addLayout(seach_layout)
        #表格组件
        table_widget = self.parent.load_data('vision')
        
        #table_widget.setFixedHeight(650)
        seach_text_area.textChanged.connect(lambda : self.parent.filter_table(seach_text_area,table_widget))#连接搜索框的信号
        #table_widget.cellClicked.connect(lambda row ,column :self.download_model(row,column,table_widget))

        #btn_add.clicked.connect(lambda : self.or_download(table_widget))
        btn_seach.toggled.connect(lambda checked: self.parent.downloaded_table(table_widget,checked))
        table_widget.cellClicked.connect(lambda row,column :self.parent.or_download(table_widget,btn_add,btn_remove,row,column))

        widget_layout.addWidget(table_widget)
        vision_widget.setLayout(widget_layout)

        return vision_widget