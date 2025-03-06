from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QLabel
from PyQt5.QtWidgets import QHBoxLayout,QVBoxLayout
from PyQt5.QtWidgets import QDialog
import ollama,asyncio,pymysql
from PyQt5.QtCore import QThread, pyqtSignal,Qt
from PyQt5.QtGui import QTextCursor, QTextBlockFormat

from HeaderWidget import HeaderWidget
from ShowWidget import ShowWidget
from ChatWidget import ChatWidget
class Data:
    db_message = []

# 在home_page类中使用这些新类
class home_page(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.resize(1200,900)
        self.home_layout = QVBoxLayout(self)
        
        # 创建widget实例
        self.header_widget = HeaderWidget(self)
        self.show_widget = ShowWidget(self)
        self.chat_widget = ChatWidget(self)
        
        # 加载组件
        self.home_layout.addLayout(self.header_widget.init_layout())
        self.home_layout.addWidget(self.show_widget.init_layout())
        self.home_layout.addLayout(self.chat_widget.init_layout())
    
    def reset_chat(self):
        print(1111111111111111)
        self.home_layout.takeAt(1)
        self.home_layout.takeAt(1)
        self.home_layout.addWidget(self.show_widget.init_layout())
        self.home_layout.addLayout(self.chat_widget.init_layout())
    
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
            #print(db_message_json)
            with connect.cursor() as cursor:
                sql_check = """
                SELECT conversation_id 
                FROM conversations 
                WHERE JSON_SEARCH(messages, 'one', %s, NULL, '$[*].content') IS NOT NULL;
                """
                content_to_check = self.db_messages[0]["content"]
                cursor.execute(sql_check, (content_to_check,))
                result = cursor.fetchone()

                if result:
                    # 如果存在相同的 content，更新记录
                    sql_update = """
                    UPDATE conversations
                    SET messages = %s
                    WHERE conversation_id = %s;
                    """
                    messages_json = json.dumps(self.db_messages)
                    cursor.execute(sql_update, (messages_json, result[0]))
                    print(f"更新了 conversation_id 为 {result[0]} 的记录")
                else:
                    # 如果不存在，插入新记录
                    sql_insert = """
                    INSERT INTO conversations (messages) VALUES (%s);
                    """
                    messages_json = json.dumps(self.db_messages)
                    cursor.execute(sql_insert, (messages_json,))
                    print("插入了新记录")

                connect.commit()
        except pymysql.MySQLError as e:
            print(e)
        finally:
            connect.close()
            cursor.close()
            self.reset_chat() #保存成功后重置对话框
            self.db_messages = []

        print('保存成功')
    
    def load_message(self):
        """#历史加载"""
       # print(self.db_messages[0]["content"])
        
        connect = pymysql.connect(host='localhost',
                                    user='root',
                                    password='xxlong727',
                                    database='model_ollama',
                                    charset='utf8mb4')
        try:
            with connect.cursor() as cursor:
                sql = """
                SELECT messages FROM conversations;
                    """
                cursor.execute(sql)
                db_message = cursor.fetchall()
                connect.commit()   
        except pymysql.MySQLError as e:
                print(e)
        finally:
                connect.close()
        """
        将中间的文本框作为参数，传入
        使用append_message()方法，将对话传入文本框
        """
        load_show = load_page(self.text_area,db_message)
        while True:
            if not load_show.exec_():
                self.db_messages = Data.db_message
                return

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
        #print(self.db_messages)
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
        #print(result)
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


class load_page(QDialog):
    """选择指定对话历史界面"""
    def __init__(self,text_area,db_message):
        super().__init__()
        self.setWindowTitle("加载页面")
        self.setFixedSize(500,500)
        
        self.text_area = text_area
        self.db_message = db_message


        layout = QVBoxLayout(self)
        for title,i,content in zip(self.title(), range(len(self.title())), self.content()): #每个循环传递一组数据

            tip_one = tip_message(self,self.text_area,title,i,content)
                
            layout.addWidget(tip_one)
            
        layout.addStretch()
        #self.show()

    def title(self):
        import json
        title = []
        for me in self.db_message:
            mess = json.loads(me[0])
            title.append(mess[0]['content'])

            #print(mess[0]['content'])  #标题
            #print(type(mess))
        return title
    def content(self):
        import json
        content = []
        for me in self.db_message:
            mess = json.loads(me[0])
            content.append(mess)
        return content
"""
            1. 从数据库中读取json格式的对话
            2. 转为messages列表
            3. 使用第一个提问当做选择的主题
            4. 创建另一个窗口用作选择某一条历史对话，携带具体的第几条，用作删除的索引
            5. 点击其中一条，将其内容显示在对话框中
            6.设计一个删除按钮，删除该条对话
            """

class tip_message(QWidget):
    """单个历史小组件，包括选择，删除按键"""
    def __init__(self,load_page,text_area, title, index,content):
        super().__init__()
        self.setBaseSize(500,50)
        self.layout_tip = QHBoxLayout(self)

        self.load_page = load_page
        self.text_area = text_area
        self.title = title # 历史记录的第一个 问题
        self.index = index  #第几个历史记录
        self.content = content


        self.text_rm_do()
    def text_rm_do(self):
        
        text_label = QLabel(f"{self.title}")
        btn_rm = QPushButton("删除")
        btn_do = QPushButton("选择")

        btn_rm.setFixedSize(40,25)
        btn_do.setFixedSize(40,25)
        self.layout_tip.addWidget(text_label)
        self.layout_tip.addWidget(btn_rm)
        self.layout_tip.addWidget(btn_do)

        btn_do.clicked.connect(lambda: self.choose())
        btn_rm.clicked.connect(lambda: self.remove())
        """
        将中间的文本框作为参数，传入
        使用append_message()方法，将对话传入文本框"""
    def choose(self):
        self.text_area.clear()
        for i,text in enumerate(self.content):
            if i%2 ==0:
                self.append_message(text["content"],Qt.AlignRight)
            else:
                self.append_message(text["content"],Qt.AlignLeft)
                
        Data.db_message = self.content

        self.load_page.close()
    def remove(self):
        connect = pymysql.connect(host='localhost',
                                  user='root',
                                  password='xxlong727',
                                  database='model_ollama',
                                  charset='utf8mb4')
        try:
            with connect.cursor() as cursor:
                print(11111111111)
                sql ="""
                    delete FROM conversations
                    WHERE JSON_SEARCH(messages, 'one', %s, NULL, '$[*].content') IS NOT NULL;
                    """
                search_pattern = f"%{self.title}%"
                cursor.execute(sql,(search_pattern,))
                connect.commit()
                self.close()
                print("删除")
        except pymysql.MySQLError as e:
            print(e)
        finally:
            connect.close()
        """
        保存逻辑，需要判断是不是已经存入的数据，
        通过第一个问题的判断
        添加进保存的方法中"""


    def append_message(self, text, align):
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