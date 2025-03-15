from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QLabel
from PyQt5.QtWidgets import QHBoxLayout,QVBoxLayout
from PyQt5.QtWidgets import QDialog,QFormLayout
from PyQt5.QtWidgets import QLabel, QScrollArea,QLineEdit


Config =['host','user','password','database','charset','path'] 

class setting_page(QWidget):
    def __init__(self,):
        super().__init__()
        self.resize(700,700)

        layout = QVBoxLayout(self)
        
        self.config_content = []
        self.init_config()

        layout.addLayout(self.head_layout())
        layout.addWidget(QLabel("数据库配置"))
        layout.addWidget(self.scroll_widget())
        layout.addStretch()

    def head_layout(self):
        """最上面的按钮"""
        head_layout = QHBoxLayout()#设置水平组件
        
        btn_save = QPushButton("保存更改")
        btn_save.setFixedSize(150,80)
        btn_save.clicked.connect(lambda:self.save_config())
        head_layout.addStretch()
        head_layout.addWidget(btn_save)
        return head_layout
    def scroll_widget(self):
        config_name =['host','user','password','database','charset','path'] 

        scroll_area = QScrollArea()#储存各项设置的组件

        #content_widget = QWidget()
        content_layout = QFormLayout() 
        self.setting_line = []#创建一个列表用于保存每一个行对象
        for name,content in zip(config_name,self.config_content):
            text_line = QLineEdit()
            text_line.setText(content)#设置为预设值
            text_line.setFixedHeight(50)
            self.setting_line.append(text_line)
            content_layout.addRow(QLabel(name),text_line)
        scroll_area.setLayout(content_layout)
        return scroll_area
    def save_config(self):
        con = [i.text() for i in self.setting_line]
        self.config.save(*con)
        
    def init_config(self):
        """初始化配置文件"""
        self.config = AppConfig()
        self.config_content = [self.config.db_host,self.config.db_user,self.config.db_passward,self.config.db_database,self.config.db_charset,self.config.config_path]


import configparser
import os,pymysql

class AppConfig:
    def __init__(self, config_file="config.ini"):
        self.config_file = config_file
        self.config = configparser.ConfigParser()

        # 检查配置文件是否存在
        if not os.path.exists(config_file):
            # 如果文件不存在，创建一个默认的配置文件
            self.create_default_config()

        # 读取配置文件
        self.config.read(config_file)

        # 加载配置变量
        self.db_host = self.config.get("DEFAULT", "host", fallback="localhost")
        self.db_user = self.config.get("DEFAULT", "user", fallback="root")
        self.db_passward = self.config.get("DEFAULT", "password", fallback="xxlong727")
        self.db_database = self.config.get("DEFAULT", "database", fallback="model_ollama")
        self.db_charset = self.config.get("DEFAULT", "charset", fallback="utf8mb4")
        self.config_path = self.config.get("DEFAULT", "path", fallback="config/settings.ini")
    def create_default_config(self):
        # 创建默认的配置文件
        self.config["DEFAULT"] = {
            "host": "localhost",
            "user": "root",
            "password": "xxlong727",
            "database": "model_ollama",
            "charset": "utf8mb4",
            "path":"config/settings.ini"
        }
        with open(self.config_file, "w") as configfile:
            self.config.write(configfile)

    def save(self,db_host,db_user,db_passward,db_database,db_charset,config_path):
        # 保存当前配置到文件

        db = {'host':db_host,
                'user':db_user,
                'password':db_passward,
                'database':db_database,
                'charset':db_charset,
        }
        print(123441414)
        try:
        # 尝试连接到数据库
            with pymysql.connect(**db) as connect:
                print("数据库连接成功！")
                self.config.set("DEFAULT", "host", db_host)
                self.config.set("DEFAULT", "user", db_user)
                self.config.set("DEFAULT", "password",db_passward)
                self.config.set("DEFAULT", "database", db_database)
                self.config.set("DEFAULT", "charset", db_charset)
                self.config.set("DEFAULT", "path",config_path)
                print("保存成功")
        except pymysql.MySQLError as e:
            print(f"数据库连接失败: {e}")


        
      
        with open(self.config_file, "w") as configfile:
            self.config.write(configfile)
    
    def get_config(self):
        return {'host':self.db_host,
                'user':self.db_user,
                'password':self.db_passward,
                'database':self.db_database,
                'charset':self.db_charset,
        }
# 使用示例
# config = AppConfig()
# print(config.log_level)  # 输出：DEBUG

# # 修改变量
# config.log_level = "INFO"
# config.save()  # 保存到配置文件
"""


        self.db_config = {
            'host': 'localhost',       # 数据库主机地址
            'user': 'root',            # 数据库用户名
            'password': 'xxlong727',   # 数据库密码
            'database': 'model_ollama',# 数据库名
            'charset': 'utf8mb4',      # 字符编码
            'path':                    #配置文件位置

            }
         设置界面：
         1. 使用QScrollArea滚动组件,储存QFormLayout表单组件
         2. 实现数据库的配置修改，使用  .ini文件储存配置文件实现保存"""