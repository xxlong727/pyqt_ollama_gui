import sys
import os
from PyQt5.QtWidgets import QApplication,QWidget,QFrame
from PyQt5.QtWidgets import QHBoxLayout,QVBoxLayout
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QLineEdit,QTextEdit
from PyQt5.QtWidgets import QTableWidget,QSpacerItem, QSizePolicy
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtWidgets import QLabel, QSplitter
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QMenu,QAction
from PyQt5.QtCore import Qt

BASE_PATH =  os.path.dirname(os.path.abspath(__file__))

class built_window(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("gui")
        self.resize(1200,700)
        self.setMinimumSize(500,500)
       # self.
       # print(BASE_PATH)
        layout = QHBoxLayout()

        splitter = QSplitter(Qt.Horizontal)

        splitter.addWidget(self.init_left())
      #  layout.addStretch()
        splitter.setMinimumSize(0, 100)

        splitter.addWidget(self.init_side())
        splitter.setChildrenCollapsible(False)#不能通过拖动分隔条来压缩这些子部件
        layout.addWidget(splitter)
       # layout.addStretch()


        self.setLayout(layout)#将组件添加到窗口


    #左边视图
    def init_left(self):
        #frame 方框
        frame1 = QFrame(self)
        frame1.setFrameShape(QFrame.Box)
        frame1.setLineWidth(1)
        frame1.setBaseSize(200,900)
      #  frame1.setMinimumWidth(100)
        left_layout = QVBoxLayout(frame1)

        btn_start = QPushButton("初始化")
        btn_start.setFixedHeight(100)
       # btn_start.setMinimumWidth(150)
        btn_choose = QPushButton("选择模型")
        btn_choose.setFixedHeight(100)
        btn_choose.clicked.connect(self.choose_model)#绑定事件
    
        btn_download = QPushButton("下载模型")
        btn_download.setFixedHeight(100)

        btn_theme = QPushButton("切换主题")
        btn_theme.setFixedHeight(100)

        left_layout.addWidget(btn_start)
        left_layout.addWidget(btn_choose)
        left_layout.addWidget(btn_download)
        left_layout.addWidget(btn_theme)
        left_layout.addStretch()
        #空间占用项目
       # item_space = QSpacerItem(100,100)

       # left_layout.addItem(item_space)
        return frame1
  
    def choose_model(self):

        from button_actions import choose_btn
        win_choose = choose_btn(self)
        win_choose.exec_()



#中部视图
    def init_side(self):
        #第一层方框
        frame = QFrame(self)
        frame.setFrameShape(QFrame.Box)
        frame.setLineWidth(1)
        frame.setBaseSize(950,900)
       
        side_layout = QVBoxLayout(frame)#frame方框遵守竖直排布

        #第二层方框1  header栏
        self.side_header_frame(frame)
        #方框2 显示文本栏
        self.side_text_frame(frame)
        #方框3 发送栏
        self.side_chat_frame(frame)
       # side_layout.addStretch()
       # item_space = QSpacerItem(700,300)
       # side_layout.addItem(item_space)
        return frame

#创建二级顶部方框功能键                                                                                                                                                                                                                                                                  
    def side_header_frame(self, frame):
        frame_header = QFrame(frame)
        frame_header.setFrameShape(QFrame.Box)
        frame_header.setLineWidth(0)
        frame_header.setBaseSize(900,100)

        side_layout = QHBoxLayout(frame_header) #继承顶部方框

        btn_1 = QPushButton("1")
        btn_1.setFixedSize(50,100)
        btn_2 = QPushButton("2")
        btn_3 = QPushButton("3")
        btn_4 = QPushButton("4")

        side_layout.addWidget(btn_1)
        side_layout.addWidget(btn_2)
        side_layout.addWidget(btn_3)
        side_layout.addWidget(btn_4)

        frame.layout().addWidget(frame_header)
#创建文本框
    def side_text_frame(self,frame):

        text_frame = QFrame(frame)
        text_frame.setLineWidth(0)
        text_frame.setFrameShape(QFrame.Box)
        text_frame.setBaseSize(900,650)
       
        text_layout = QHBoxLayout(text_frame)

        text_area = QTextEdit()
        text_area.setReadOnly(True)
        text_layout.addWidget(text_area)
        frame.layout().addWidget(text_frame)#.layout()获取frame当前的布局，再添加
#创建对话框
    def side_chat_frame(self,frame):
        chat_frame = QFrame(frame)

        chat_frame.setLineWidth(0)
        chat_frame.setFrameShape(QFrame.Box)
        chat_frame.setBaseSize(900,200)
        chat_frame.setFixedHeight(150)

        chat_layout = QHBoxLayout(chat_frame)
        #对话栏
        chat_area = QTextEdit()
        chat_area.setBaseSize(800,100)
       # chat_area.setMinimumHeight(100)
        chat_layout.addWidget(chat_area)


        btn_send = QPushButton("发送")
        btn_send.setFixedSize(175,75)
        chat_layout.addWidget(btn_send)
        frame.layout().addWidget(chat_frame)



if __name__ == '__main__':
    #创建QApplication类的实例
    app = QApplication(sys.argv)
    w = built_window()#实例化对象
#显示窗口
    w.show()
# 确保所有事件循环和线程都被正确清理和关闭
    sys.exit(app.exec_())
