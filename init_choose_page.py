import subprocess
from PyQt5.QtWidgets import  QWidget, QPushButton, QVBoxLayout, QLabel
from PyQt5.QtWidgets import QHBoxLayout,QVBoxLayout,QStackedWidget
from PyQt5.QtWidgets import QTableWidget
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtCore import QThread

import pymysql,subprocess

from ToolsWidget import ToolsWidget
from VisionWidget import VisionWidget
from MoreWidget import MoreWidget

Width_type = {'more':100,'tools':50,'vision':20}
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

        self.init_table_tools = ToolsWidget(self)
        self.init_table_vision = VisionWidget(self)
        self.init_table_more = MoreWidget(self)

        self.table_stack.addWidget(self.init_table_tools.Init())#创建tools界面
        self.table_stack.addWidget(self.init_table_vision.Init())#创建vision界面
        self.table_stack.addWidget(self.init_table_more.Init())#更多模型

        layout.addWidget(self.table_stack)
       

    def init_act(self):

        act_layout = QHBoxLayout()

        lable = QLabel("下载选择")
        lable.setFixedHeight(100)

        btn_reset = QPushButton("刷新")
        btn_reset.setFixedHeight(100)
        act_layout.addWidget(lable)
        act_layout.addStretch()
        act_layout.addWidget(btn_reset)

        btn_reset.clicked.connect(self.reset_table)#刷新表格

        return act_layout
    def reset_table(self):#刷新表格
        self.table_stack.removeWidget(self.table_stack.widget(0))
        self.table_stack.removeWidget(self.table_stack.widget(0))
        self.table_stack.removeWidget(self.table_stack.widget(0))

        self.table_stack.addWidget(self.init_table_tools())
        self.table_stack.addWidget(self.init_table_vision())
        self.table_stack.addWidget(self.init_table_more())
        
        self.table_stack.setCurrentIndex(0)

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
    
    def filter_table(self,seach_text_area,table_widget):#搜索功能
        search_text = seach_text_area.toPlainText().strip()
        if search_text:
            for row in range(table_widget.rowCount()):#隐藏所有行
                table_widget.setRowHidden(row, True)

            for row in range(table_widget.rowCount()):
                item = table_widget.item(row, 0)
                if item and search_text.lower() in item.text().lower():  # 不区分大小写
                    table_widget.setRowHidden(item.row(), False)#显示搜索到的行
        elif not search_text:
            for row in range(table_widget.rowCount()):
                table_widget.setRowHidden(row, False)
    
    def remove_model(self,row,table_widget):#删除模型
        model_name = table_widget.item(row, 0).text()
        model_size = table_widget.item(row, 2).text().split("-")[0]
        name_size = model_name + ":" + model_size
        subprocess.run(["ollama", "rm",name_size], capture_output=True, text=True, check=True)
        connect = pymysql.connect(host='localhost',
                                    user='root',
                                    password='xxlong727',
                                    database='model_ollama',
                                    charset='utf8mb4')
        with connect.cursor() as cursor:
            sql = """
                    UPDATE parameters 
                    JOIN model ON model.model_id = parameters.model_id 
                    SET parameters.isdownloaded = 0 
                    WHERE model.name = %s AND parameters.size_storage = %s;
                    """
            cursor.execute(sql, (model_name, model_size))
            connect.commit()
            cursor.close()
            connect.close()

    def or_download(self,tabel_widget,btn_add,btn_remove,row,column):#判断是否下载
        #点击下载才进行下载
        from utils.download import Download
        #print(11111111111111111111111)
        download = Download()
        down_thread = QThread()

        download.moveToThread(down_thread)#将下载功能移动到子线程
        down_thread.started.connect(lambda :download.download_model(row,column,tabel_widget))#线程启动绑定下载

        download.finished.connect(down_thread.quit)
        download.finished.connect(download.deleteLater)
        down_thread.finished.connect(down_thread.deleteLater)

        btn_add.clicked.connect(lambda :down_thread.start())#点击下载按钮，启动线程
        btn_remove.clicked.connect(lambda :self.remove_model(row,tabel_widget))#删除模型

    # def download_model(self,row,column,table_widget):#下载功能
         
    #     model_name = table_widget.item(row, 0).text()
    #     model_size = table_widget.item(row, 2).text().split("-")[0]
    #     name_size = model_name + ":" + model_size
    #     #print(name_size)
    #     print("下载ing")
    #     try:
    #     # 使用 subprocess.run 运行命令
    #         subprocess.run(["ollama", "run",name_size], capture_output=True, text=True, check=True)
    #         return
    #         #print(f"Command output:\n{result.stdout}")
    #     except subprocess.CalledProcessError as e:
    #         print(f"An error occurred: {e}")
    #         print(f"Error output:\n{e.stderr}")
  
    def load_data(self,type):
        table_widget = QTableWidget(Width_type[f"{type}"],7)
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
                query = f"""
                        SELECT model.model_id, model.name, model.description, model.home, parameters.isdownloaded, model.type,
                            parameters.para_id,parameters.size_storage
                        FROM model
                        JOIN parameters ON model.model_id = parameters.model_id
                        WHERE model.type = '{type}';
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
                    row += 1
            except pymysql.MySQLError as e:
                print(f"Error fetching data: {e}")

        return table_widget
    

    def downloaded_table(self,table_widget,checked):#已下载功能
        
        if checked:
            
            try:
                # 运行 ollama list 命令并捕获输出
                result = subprocess.run(["ollama", "list"], capture_output=True, text=True, check=True)
                # 打印命令输出
                # print(f"Command output:\n{result.stdout}")
                # 返回命令输出
                #time.sleep()
            except subprocess.CalledProcessError as e:
                print(f"An error occurred: {e}")
                print(f"Error output:\n{e.stderr}")
            output = result.stdout # 获取命令输出的结果
            lines = output.strip().split("\n")[3:]
            
            for row in range(table_widget.rowCount()):#隐藏所有行
                table_widget.setRowHidden(row, True)
            if not lines:  # 如果没有数据
                for row in range(table_widget.rowCount()):
                    table_widget.setRowHidden(row, False)
                #print(lines)
            
            downloaded_models = set() # 创建一个集合，用于存储已下载的模型
            for line in lines:
                name_size = line.split('b')[0] + 'b'
                name = name_size.split(':')[0]
                size = name_size.split(':')[1]
                downloaded_models.add((name, size))

            #print(downloaded_models)
            # 遍历表格，更新 isdownloaded 字段
            #print(table_widget.rowCount())
            for row in range(table_widget.rowCount()):
                #print(11111111111111)
                item_name = table_widget.item(row, 0)
                item_size = table_widget.item(row, 2)
                
              #  print(f"{item_name.text(),item_size.text()}")
                
                if item_name is None or item_size is None:#跳过空行
                        #print(f"Skipping row {row} due to missing data.")
                        continue  # 跳过当前行
                       
                
                if item_name and item_size:
                    name = item_name.text().lower()
                    size = item_size.text().split('-')[0]  # 假设 size 是 "3b-398MB" 格式
                    
                    if (name, size) in downloaded_models:
                        #print(name,size)
                        #print(downloaded_models)
                        #print(item_size.text())
                        # 如果当前行的模型已下载，设置 isdownloaded 为 1
                        try :
                            connect = pymysql.connect(host='localhost',
                                    user='root',
                                    password='xxlong727',
                                    database='model_ollama',
                                    charset='utf8mb4')
                            with connect.cursor() as cursar:
                                query = """
                                UPDATE parameters 
                                JOIN model ON model.model_id = parameters.model_id 
                                SET parameters.isdownloaded = 1 
                                WHERE model.name = %s AND parameters.size_storage = %s;
                                """
                                #pattern = f"%{size}-%"
                                cursar.execute(query, (name, item_size.text()))
                                connect.commit()
                                table_widget.setRowHidden(row, False) 
                        finally:
                            cursar.close()
                    else:
                        # 如果当前行的模型未下载，设置 isdownloaded 为 0
                        #print(name,size)
                        connect = pymysql.connect(host='localhost',
                                  user='root',
                                  password='xxlong727',
                                  database='model_ollama',
                                  charset='utf8mb4')
                        try:
                            with connect.cursor() as cursar:
                                query = """
                                UPDATE parameters 
                                JOIN model ON model.model_id = parameters.model_id 
                                SET parameters.isdownloaded = 0 
                                WHERE model.name = %s AND parameters.size_storage = %s;
                                """
                            # pattern = f"%{size}-%"
                                cursar.execute(query, (name, item_size.text()))
                                connect.commit()
                        finally:
                            cursar.close()
        elif not checked:#取消选中，显示所有行
            for row in range(table_widget.rowCount()):
                table_widget.setRowHidden(row, False) 
