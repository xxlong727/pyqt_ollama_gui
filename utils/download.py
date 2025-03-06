import subprocess,pymysql,time
from PyQt5.QtCore import QObject, QThread, pyqtSignal, pyqtSlot

class Download(QObject):
    finished = pyqtSignal()# 结束信号
    @pyqtSlot(int,int,object)# 装饰器，用于绑定槽函数

    def download_model(self,row,column,table_widget):#下载功能
            
            model_name = table_widget.item(row, 0).text()
            model_size = table_widget.item(row, 2).text().split("-")[0]
            name_size = model_name + ":" + model_size
            #print(name_size)
            print("下载ing")
            try:
            # 使用 subprocess.Popen 运行命令
                process= subprocess.Popen(["ollama", "pull", name_size], stdout=None, stderr=None, text=True)
                
            except subprocess.CalledProcessError as e:
                print(f"An error occurred: {e}")
                print(f"Error output:\n{e.stderr}")
            finally:
                connect = pymysql.connect(host='localhost',
                                    user='root',
                                    password='xxlong727',
                                    database='model_ollama',
                                    charset='utf8mb4')
                with connect.cursor() as cursor:
                    sql = """
                            UPDATE parameters 
                            JOIN model ON model.model_id = parameters.model_id 
                            SET parameters.isdownloaded = 1 
                            WHERE model.name = %s AND parameters.size_storage = %s;
                            """
                    cursor.execute(sql, (model_name, table_widget.item(row, 2).text()))
                    connect.commit()
                    cursor.close()
                    connect.close
                    print("下载完成")
               

