import sys
import os
from PyQt5.QtWidgets import QApplication,QWidget,QFrame
from PyQt5.QtWidgets import QHBoxLayout,QVBoxLayout
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QLineEdit,QTextEdit
from PyQt5.QtWidgets import QTableWidget,QSpacerItem, QSizePolicy
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QMenu,QAction
from PyQt5.QtCore import Qt


class built_window(QWidget):

    def __init__(self,):
        super().__init__()
        self.setWindowTitle("gui")
        self.resize(1200,700)
       # self.

        layout = QHBoxLayout()
        layout.addWidget(self.init_left())
      #  layout.addStretch()
        layout.addWidget(self.init_side())
       # layout.addStretch()


        self.setLayout(layout)#将组件添加到窗口


    #左边视图
    def init_left(self):
        #frame 方框
        frame1 = QFrame(self)
        frame1.setFrameShape(QFrame.Box)
        frame1.setLineWidth(5)
        frame1.setBaseSize(200,900)

        left_layout = QVBoxLayout(frame1)

        btn_start = QPushButton("初始化")
        btn_choose = QPushButton("选择模型")
        btn_download = QPushButton("下载模型")
        btn_theme = QPushButton("切换主题")

        left_layout.addWidget(btn_start)
        left_layout.addWidget(btn_choose)
        left_layout.addWidget(btn_download)
        left_layout.addWidget(btn_theme)
        #空间占用项目
       # item_space = QSpacerItem(100,100)

       # left_layout.addItem(item_space)
        return frame1
    #中部视图
    def init_side(self):
        #第一层方框
        frame = QFrame(self)
        frame.setFrameShape(QFrame.Box)
        frame.setLineWidth(5)
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
        frame_header.setLineWidth(5)
        frame_header.setBaseSize(900,100)

        side_layout = QHBoxLayout(frame_header) #继承顶部方框

        btn_1 = QPushButton("1")
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
        text_frame.setLineWidth(5)
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

        chat_frame.setLineWidth(5)
        chat_frame.setFrameShape(QFrame.Box)
        chat_frame.setBaseSize(900,100)

        chat_layout = QHBoxLayout(chat_frame)
        #对话栏
        chat_area = QTextEdit()
        chat_layout.addWidget(chat_area)

        btn_send = QPushButton("发送")
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
