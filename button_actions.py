from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QDialog, QVBoxLayout, QLabel
from PyQt5.QtWidgets import QHBoxLayout,QVBoxLayout
from PyQt5.QtWidgets import QLineEdit,QTextEdit
from PyQt5.QtWidgets import QTableWidget,QSpacerItem, QSizePolicy
from PyQt5.QtWidgets import QTableWidgetItem
#选择模型类
class choose_btn(QDialog):
    def __init__(self, parent =None):
        super().__init__(parent)

        self.setWindowTitle("选择模型")
        self.resize(500,250)

        layout = QVBoxLayout(self)

        layout.addLayout(self.init_search())#添加搜索

        layout.addLayout(self.init_table())#添加表格

        layout.addStretch()
    

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

        table_widget = QTableWidget(2,2)
        table_widget.setColumnWidth(1,600)

        btn_add = QPushButton("确认")
        table_layout.addWidget(btn_add)
        table_layout.addStretch()
        table_layout.addWidget(table_widget)

        return table_layout
