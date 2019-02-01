from bs4 import BeautifulSoup
import requests
import re
import os
import shutil
os.makedirs('japan_stock')
stock_num=2702

r = requests.get('https://www.nikkei.com/markets/kigyo/disclose/?kwd='+str(stock_num)+'&SelDateDiff=11')
soup = BeautifulSoup(r.text)

res = r"平成(.*?)target"
urls = re.findall(res, str(soup))
for i in range(len(urls)):
    the = r"t=(.*?)\""
    pp = re.findall(the, str(urls[i]))
    name=r"(.*?)短信"
    names = re.findall(name, str(urls[i]))
    import requests, zipfile, io
    r = requests.get(pp[0])
    z = zipfile.ZipFile(io.BytesIO(r.content))
    z.extractall()


    #获取文件名

    for i in range(len(os.listdir(os.path.abspath(os.curdir)+'/XBRLData/Summary/' ))):
        if 'htm' in os.listdir(os.path.abspath(os.curdir)+'/XBRLData/Summary/' )[i]:
            file_name=os.listdir(os.path.abspath(os.curdir)+'/XBRLData/Summary/' )[i]
    #找到文件路径
    path=os.path.join(os.path.abspath(os.curdir),'/XBRLData/Summary/')
    file_path=os.path.join(path,file_name)


    print(file_path)
    file_path=os.getcwd()+file_path
    #重命名
    os.rename(file_path,os.path.abspath(os.curdir)+'/XBRLData/Summary/' +str(stock_num)+names[0]+'.htm')
    #复制
    file_path=os.path.join(path,file_path)
    file_path=os.getcwd()+file_path
    shutil.copy(os.path.abspath(os.curdir)+'/XBRLData/Summary/' +str(stock_num)+names[0]+'.htm',"japan_stock")
    #删除文件夹
    shutil.rmtree(os.path.abspath(os.curdir)+'/XBRLData')



from bs4 import BeautifulSoup
import requests
import re
import os
import shutil
try:
    os.makedirs('japan_stock')
except:
     shutil.rmtree('japan_stock')
     os.makedirs('japan_stock')
stock_num=2702
r = requests.get('https://www.nikkei.com/markets/kigyo/disclose/?kwd='+str(stock_num)+'&SelDateDiff=11')
soup = BeautifulSoup(r.text)

res = r"平成(.*?)target"
urls = re.findall(res, str(soup))
for i in range(len(urls)):
    the = r"t=(.*?)\""
    pp = re.findall(the, str(urls[i]))
    name=r"(.*?)短信"
    names = re.findall(name, str(urls[i]))
    #print(names)
    import requests, zipfile, io
    r = requests.get(pp[0])
    z = zipfile.ZipFile(io.BytesIO(r.content))
    z.extractall()

    #获取文件名

    for i in range(len(os.listdir(os.path.abspath(os.curdir)+'/XBRLData/Summary/' ))):
        if 'htm' in os.listdir(os.path.abspath(os.curdir)+'/XBRLData/Summary/' )[i]:
            file_name=os.listdir(os.path.abspath(os.curdir)+'/XBRLData/Summary/' )[i]
    #找到文件路径
    path=os.path.join(os.path.abspath(os.curdir),'/XBRLData/Summary/')
    file_path=os.path.join(path,file_name)
    file_path=os.getcwd()+file_path
    print(file_path)
    os.rename(file_path,os.path.abspath(os.curdir)+'/XBRLData/Summary/' +str(stock_num)+names[0]+'.htm')

