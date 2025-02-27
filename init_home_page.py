from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel
from PyQt5.QtWidgets import QHBoxLayout,QVBoxLayout
from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtWidgets import QComboBox
import ollama,asyncio,pymysql
from PyQt5.QtCore import QThread, pyqtSignal,Qt
from PyQt5.QtGui import QTextCursor, QTextBlockFormat


class home_page(QWidget):
    def __init__(self, parent =None):
        super().__init__(parent)
        self.resize(1200,900)
        self.home_layout = QVBoxLayout(self)#总空间
        #加载组件
        self.home_layout.addLayout(self.init_head())
        self.home_layout.addWidget(self.init_show())
        self.home_layout.addLayout(self.init_chat())
    
    def init_head(self):
        """#顶部控件"""
        header_layout = QHBoxLayout()

        btn_new = QPushButton("新建对话")
        #btn_change = QPushButton("切换模型")
        btn_store = QPushButton("保存对话")
        btn_load = QPushButton("历史加载")

        btn_new.setFixedHeight(100)
        #btn_change.setFixedHeight(100)
        btn_store.setFixedHeight(100)
        btn_load.setFixedHeight(100)

        btn_new.clicked.connect(lambda: self.reset_chat())
        btn_store.clicked.connect(lambda: self.message_to_db())


        header_layout.addWidget(btn_new)
        #header_layout.addWidget(btn_change)
        header_layout.addWidget(btn_store)
        header_layout.addWidget(btn_load)
        return header_layout
    
    def reset_chat(self):
        print(1111111111111111)
        self.home_layout.takeAt(1)
        self.home_layout.takeAt(1)
        self.home_layout.addWidget(self.init_show())
        self.home_layout.addLayout(self.init_chat())
    
    def message_to_db(self):
        """#保存对话"""
        import json
        if not self.db_messages:
            return
        
        db_message_json = json.dumps(self.db_messages,ensure_ascii=False)
        
        connect = pymysql.connect(host='localhost',
                                  user='root',
                                  password='xxlong727',
                                  database='model_ollama',
                                  charset='utf8mb4')
        try:
            print(db_message_json)
            with connect.cursor() as cursor:
                sql = """
                INSERT INTO conversations (messages) VALUES (%s);
                """
                cursor.execute(sql,(db_message_json,))
                connect.commit()
            
        except pymysql.MySQLError as e:
            print(e)
        finally:
            connect.close()
            cursor.close()
            self.reset_chat() #保存成功后重置对话框
            self.db_messages = []

        print('保存成功')
       

    def init_show(self):
        """ #中间文本显示   """
        self.text_area = QTextEdit()
        self.text_area.setReadOnly(True)
        self.text_area.setFontPointSize(15)
        self.content = None

        return self.text_area

   
    def init_chat(self):
        """ #底部对话"""
        chat_layout = QHBoxLayout()

        chat_area = QTextEdit()
        chat_area.setPlaceholderText("请输入对话内容")
        chat_area.setFontPointSize(15)
        chat_area.setBaseSize(800,100)
        chat_area.setMaximumHeight(150)
        chat_layout.addWidget(chat_area)

        
        chat_btn_layout = QVBoxLayout() #右侧的三个排布
        choose_layout = QHBoxLayout()

        btn_choose_file = QPushButton("选择文件")

        self.db_messages = []
        self.file_paths = None

        label = QLabel("模型选择")#创建标签
        model_path_label = QLabel("未选择文件")

        btn_choose_file.clicked.connect(lambda: self.open_file_dialog(model_path_label)) #绑定事件


        cbox_change = QComboBox()# 创建下拉框
        cbox_change.addItems(self.get_model())
        cbox_change.currentTextChanged.connect(self.on_model_changed)  # 连接信号到槽函数


        self.current_model = cbox_change.currentText()#设置初始值

        #cbox_change.addItem("切换模型")
        btn_send = QPushButton("发送")
        btn_send.setFixedSize(175,75)
        btn_send.clicked.connect(lambda: self.send_message(chat_area,self.current_model,self.or_model(self.current_model))) #绑定事件
        #btn_change.setFixedSize(175,75)

        choose_layout.addWidget(label)
        choose_layout.addWidget(btn_choose_file)

        chat_btn_layout.addLayout(choose_layout)
        chat_btn_layout.addWidget(model_path_label)
        chat_btn_layout.addWidget(cbox_change)
        chat_btn_layout.addWidget(btn_send)

        chat_layout.addLayout(chat_btn_layout)

        
        return chat_layout
    def on_model_changed(self,text):
        self.current_model = text

    """如果 open_file_dialog 方法从未被调用,self.file_paths 将不会被定义，从而导致 AttributeError。"""
    def open_file_dialog(self,model_path_label): #打开文件选择对话框
        from PyQt5.QtWidgets import QFileDialog
        self.file_paths = None
        self.file_paths, _ = QFileDialog.getOpenFileNames(self, "选择多个文件", "", "图片文件(*.jpg *.png)")
        if self.file_paths:
            model_path_label.setText(self.file_paths[0])
        else:
            model_path_label.setText("未选择文件")
    #
    def send_message(self,text_area,model,type):
        message = text_area.toPlainText()
        if self.file_paths != None:
            path = self.file_paths[0]

        if not message:
            return
        
        if type !=  'vision':
            path = None

        text_area.clear()#清空输入框
        self.append_message(message, align=Qt.AlignRight)# 输入的消息添加到文本框
        messages = [
                    {
                        "role": "user",
                        "content": f"{message}",
                        "path" : path
                    },
                    ]
        self.get_message(messages[0])#保存对话

        #保存对话
            # 1. 设置一个messages列表，用于保存对话
            # 2. 调用send_message()方法时，将用户输入的消息添加到messages列表中
            # 3. 创建一个新的方法， 转为json格式，存入数据库中
        #历史加载
            # 1. 从数据库中读取json格式的对话
            # 2. 转为messages列表
            # 3. 调用send_message()方法时，将messages作为新的列表参数，并将用户输入作为新加入的数据、
            # 参考chat-with-history.py
        print(self.db_messages)
        self.worker = AsyncWorker(self.send_message_to_ollama,model, self.db_messages)
        self.worker.finished.connect(self.get_response)
        self.worker.start()

    def get_response(self,re_content,re_role): 
        """添加获得的响应进入文本框"""
        self.append_message(re_content, align=Qt.AlignLeft)

        messages = {
            "role": f"{re_role}",
            "content": f"{re_content}" 
        }
        self.get_message(messages) # 传入

    def get_message(self,message) :
        """
        将输入的,响应的数据添加进db_messages列表中
        """
        self.db_messages.append(message)

        #print(self.db_messages)


    async def send_message_to_ollama(self,model,messages):
        """发送消息到ollama"""
        from ollama import AsyncClient
        client  = AsyncClient()
        response = await client.chat(model,messages=messages)
        #print(response['message'])
        return response['message']['content'],response['message']['role']
    
    
    def or_model(self,model): 
        """#判断哪种功能模型"""
        print(model)
        connect = pymysql.connect(host='localhost',
                                  user='root',
                                  password='xxlong727',
                                  database='model_ollama',
                                  charset='utf8mb4')
        with connect.cursor() as cursor:
            sql = """
            SELECT type FROM model WHERE name = %s"""
            cursor.execute(sql,model.split(':')[0])
            connect.commit()
            result = cursor.fetchone()[0]
            #print(result)
            cursor.close()
            connect.close()
        print(result)
        return result
    
    def append_message(self, text, align=Qt.AlignLeft):
        """ 添加消息"""

        # 获取 QTextCursor
        cursor = self.text_area.textCursor()

        # 创建一个新的段落格式并设置对齐方式
        block_format = QTextBlockFormat()
        block_format.setAlignment(align)

        # 插入新段落并设置格式
        cursor.insertBlock(block_format)
        cursor.insertText(text)
        self.text_area.append('\n')
        # 将光标移动到文档末尾
        cursor.movePosition(QTextCursor.End)
        self.text_area.setTextCursor(cursor)

    def closeEvent(self, event):
        """确保线程在窗口关闭时停止"""
        if hasattr(self, 'worker') and self.worker.isRunning():
            self.worker.quit()
            self.worker.wait()
        super().closeEvent(event)

    #返回模型列表
    def get_model(self):
        from ollama import ListResponse
        ollama_model_list:ListResponse = ollama.list()

        model_list = [model.model for model in ollama_model_list.models]
        return model_list

class AsyncWorker(QThread):
    finished = pyqtSignal(str,str)
    def __init__(self, func, *args, **kwargs):
        super().__init__()
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def run(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(self.func(*self.args, **self.kwargs))
        loop.close()

        content, role = result
        self.finished.emit(content, role)
