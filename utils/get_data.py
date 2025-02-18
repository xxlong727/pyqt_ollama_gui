import requests
from lxml import etree
from lxml import html
import json
#1 解析  https://ollama.com/library  得到全部模型名  
# 解析https://ollama.com/library/llama3.1/tags
#   得到 名称 ，说明,分类 ，参数（2b，6b）等数据

model_name =[ 
    "https://ollama.com/library/llama3.2",
    "https://ollama.com/library/llama3.1",
    "https://ollama.com/library/gemma2",
    "https://ollama.com/library/qwen2.5",
    "https://ollama.com/library/phi3.5",
    "https://ollama.com/library/nemotron-mini",
    "https://ollama.com/library/mistral-small",
    "https://ollama.com/library/mistral-nemo",
    "https://ollama.com/library/deepseek-coder-v2",
    "https://ollama.com/library/mistral",
    "https://ollama.com/library/mixtral",
    "https://ollama.com/library/codegemma",
    "https://ollama.com/library/command-r",
    "https://ollama.com/library/command-r-plus",
    "https://ollama.com/library/llava",
    "https://ollama.com/library/llama3",
    "https://ollama.com/library/gemma",
    "https://ollama.com/library/qwen",
    "https://ollama.com/library/qwen2",
    "https://ollama.com/library/phi3",
    "https://ollama.com/library/llama2",
    "https://ollama.com/library/nomic-embed-text",
    "https://ollama.com/library/codellama",
    "https://ollama.com/library/mxbai-embed-large",
    "https://ollama.com/library/dolphin-mixtral",
    "https://ollama.com/library/starcoder2",
    "https://ollama.com/library/phi",
    "https://ollama.com/library/deepseek-coder",
    "https://ollama.com/library/llama2-uncensored",
    "https://ollama.com/library/qwen2.5-coder",
    "https://ollama.com/library/dolphin-mistral",
    "https://ollama.com/library/tinyllama",
    "https://ollama.com/library/yi",
    "https://ollama.com/library/dolphin-llama3",
    "https://ollama.com/library/orca-mini",
    "https://ollama.com/library/zephyr",
    "https://ollama.com/library/llava-llama3",
    "https://ollama.com/library/snowflake-arctic-embed",
    "https://ollama.com/library/starcoder",
    "https://ollama.com/library/mistral-openorca",
    "https://ollama.com/library/codestral",
    "https://ollama.com/library/vicuna",
    "https://ollama.com/library/granite-code",
    "https://ollama.com/library/wizardlm2",
    "https://ollama.com/library/wizard-vicuna-uncensored",
    "https://ollama.com/library/llama2-chinese",
    "https://ollama.com/library/codegeex4"]

class get_library(): 

    def __init__(self):
        
        url = 'https://ollama.com/library'
        self.header = {
            'User-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0'
        }

        re = requests.get(url = url,headers=self.header)
        re.encoding = 'utf-8'

        page_text = re.text 

        tree_datas = html.fromstring(page_text)
        # 使用XPath查找所有的<li>标签
        li_tags = tree_datas.xpath('//li')
        print(len(li_tags))

        tree = etree.HTML(page_text)

        for i in range(len(li_tags)-6):

            li_data = tree.xpath(f'//li[{i+1}]/a/div[1]/h2/span/text()')
            model_name.append("https://ollama.com/library/"+li_data[0])

        url_json = json.dumps(model_name,indent=4)

        with open("pyqt_ollama_gui\\utils\\url.json" , mode='w') as f:
            f.write(url_json)

def get_datas(self,header):
    
    for url in model_name:
        re = requests.get(url = url,headers=header)
        re.encoding = 'utf-8'
        page_text = re.text
        tree = etree.HTML(page_text)


        name = tree.xpath("/html/body/main/div/div[1]/div[1]/h1/a/text()")
        print(name)
        description = tree.xpath()
        Parameters = tree.xpath()
        home = tree.xpath()
        size = tree.xpath()
        isdownloaded = tree.xpath()
        mode_type = tree.xpath()

if __name__ == "__main__":

    header = {
            'User-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0'
        }
    for url in model_name:
        re = requests.get(url = url,headers=header)
        re.encoding = 'utf-8'
        page_text = re.text
        tree = etree.HTML(page_text)


        name = tree.xpath("/html/body/main/div/div[1]/div[1]/div/span/a/text()")[0].strip() 
        
        description = tree.xpath("/html/body/main/div/div[1]/div[2]/div[1]/h2/span/text()")[0].strip()

        a_tags = tree.xpath('/html/body/main/div/div[1]/section/div/div[1]/div/nav/div//a')
        # 遍历<a>标签，提取需要的信息
        parameters_size=[]
        for a in a_tags :
# 提取名称（1b和3b）
            parameters = a.xpath('.//span[@class="truncate"]/span/text()')
            if parameters:
                pass
            else:
                break  # 打印1b或3b
            # 提取大小（1.3GB和2.0GB）
            size = a.xpath('.//span[@class="text-xs text-neutral-400"]/text()')
            parameters_size.append(str(parameters[0]) +'-'+ str(size[0]))

        home = url
       # isdownloaded = tree.xpath()

       # 解析HTML
        tree = html.fromstring(page_text)

        # 获取第一个<span>标签的文本内容
        first_span_text = tree.xpath('/html/body/main/div/div[1]/div[2]/div[2]/div//span[1]/text()')

        # 检查第一个<span>标签中是否包含“vision”或“tools”
        if first_span_text and ('vision' in first_span_text[0] or 'tools' in first_span_text[0]):
            mode_type = 'vision' if 'vision' in first_span_text[0] else 'tools'
        else:
            mode_type = 'more'

        model_data ={
        name:{
            "name":name,
            "description" :description,
            "Parameters-size":parameters_size,
            "home":home,
            "isdownloaded":'',
            "type":mode_type
            }
        }

        import pymysql
        connect = pymysql.connect(host='localhost',
                                  user='root',
                                  password='xxlong727',
                                  database='model_ollama',
                                  charset='utf8mb4')
        # 插入数据
        try:
            with connect.cursor() as cursar:
                sql_one = "insert into model(name,description,home,type) values(%s,%s,%s,%s)"
                cursar.execute(sql_one,(name,description,home,0,mode_type))
        
                # 获取刚刚插入的model_id
                model_id = cursar.lastrowid
                sql_two = "insert into parameters(model_id,size_storage) values(%s,%s)"
                for parameters_size in parameters_size:
                    cursar.execute(sql_two,(model_id,parameters_size))


                connect.commit()
        except pymysql.MySQLError as e:
            print(e)

        # with connect.cursor() as cursar:
        #     sql = "select * from model"
        #     cursar.execute(sql)
        #     modeldata = cursar.fetchall()

        #     #print(modeldata)
        connect.close()