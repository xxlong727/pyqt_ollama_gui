import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget, QPushButton, QBoxLayout, QWidget, QLabel
from PyQt5.QtWidgets import QHBoxLayout,QVBoxLayout,QFrame
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("gui")
        self.resize(1500,900)
        self.setMinimumSize(500,500)
        
        # 创建 QStackedWidget
        self.stacked_widget = QStackedWidget(self)

        # 创建页面
        #待重写
        self.home_page = self.homepage("首页")
        self.choose_page = self.choosepage("选择下载模型")
       # self.download_page = self.createPage("")
        self.theme_page = self.createPage("主题")

        # 将页面添加到 QStacked_widget栈页面
        self.stacked_widget.addWidget(self.home_page)
        self.stacked_widget.addWidget(self.choose_page)
        #self.stacked_widget.addWidget(self.download_page)
        self.stacked_widget.addWidget(self.theme_page)

        # 创建左侧按钮栏
       # self.left_Panel = QWidget()   self.left_Panel
        self.left_layout = QVBoxLayout()
     
        btn_start = QPushButton("首页")
        btn_start.setFixedHeight(100)
        btn_start.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
       # btn_start.setMinimumWidth(150)
        btn_choose = QPushButton("选择下载模型")
        btn_choose.setFixedHeight(100)
        btn_choose.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
       # btn_choose.clicked.connect(self.choose_model)#绑定事件
    
        # btn_download = QPushButton("下载模型")
        # btn_download.setFixedHeight(100)
        # btn_download.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(2))

        btn_theme = QPushButton("切换主题")
        btn_theme.setFixedHeight(100)
        btn_theme.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(3))

        self.left_layout.addWidget(btn_start)
        self.left_layout.addWidget(btn_choose)
      #  self.left_layout.addWidget(btn_download)
        self.left_layout.addStretch()
        self.left_layout.addWidget(btn_theme)
        

        # 设置主窗口的布局
        self.main_layout = QHBoxLayout()#水平的

        frame1 = QFrame(self)
        frame1.setFrameShape(QFrame.Box)
        frame1.setLineWidth(1)
        frame1.setBaseSize(200,900)
        frame1.setFixedWidth(150)
        frame1.setLayout(self.left_layout)

        self.main_layout.addWidget(frame1)
        self.main_layout.addWidget(self.stacked_widget)

        # 设置中央窗口和布局
        central_Widget = QWidget()
        central_Widget.setLayout(self.main_layout)
        self.setCentralWidget(central_Widget)

    def createPage(self, title):
        page = QWidget()
        layout = QVBoxLayout(page)
        label = QLabel(title)
        layout.addWidget(label)
        return page


    def homepage(self,str):#选择模型功能

        from init_home_page import home_page
        win_home = home_page(self)
        return win_home
    
    def choosepage(self,str):#选择模型功能

            from init_choose_page import choose_page
            win_choose = choose_page(self)
            return win_choose

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())