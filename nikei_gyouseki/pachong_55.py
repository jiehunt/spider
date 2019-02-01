from bs4 import BeautifulSoup
import requests
import re
import os
import shutil

WORK_PATH = 'japan_stock'

def download_file(url):
    filename = url.split("/", -1)[-1]
    r = requests.get(url, stream=True)
    with open(filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
                f.flush()
    return filename

def zip_extract(filename):
    target_directory = '.'
    zfile = zipfile.ZipFile(filename)
    # filename =  zfile.namelist()[0]
    # print (filename)
    zfile.extractall(target_directory)


def get_xbrldata(stock_nums ):

    if stock_nums is null:
        stock_nums=[2702,2703]

    if False == os.path.exists(WORK_PATH):
        os.makedirs(WORK_PATH)

    for num in range(len(stock_num)):
        r = requests.get('https://www.nikkei.com/markets/kigyo/disclose/?kwd='+str(stock_num[num])+'&SelDateDiff=11')
        soup = BeautifulSoup(r.text,features="lxml" )

        res = r"平成(.*?)target"
        urls = re.findall(res, str(soup))
        for i in range(len(urls)):
            the = r"t=(.*?)\""
            pp = re.findall(the, str(urls[i]))
            name=r"(.*?)短信"
            names = re.findall(name, str(urls[i]))
            import requests, zipfile, io

            download_file(pp[0])
            zipname = pp[0].split("/", -1)[-1]
            zip_extract(zipname)


            # r = requests.get(pp[0])
            # z = zipfile.ZipFile(io.BytesIO(r.content))
            # z.extractall()

            #获取文件名
            # for i in range(len(os.listdir(os.path.abspath(os.curdir)+'/XBRLData/Summary/' ))):
            #     print (i)
            #     if 'htm' in os.listdir(os.path.abspath(os.curdir)+'/XBRLData/Summary/' )[i]:
            #         file_name=os.listdir(os.path.abspath(os.curdir)+'/XBRLData/Summary/' )[i]
            # #找到文件路径
            # path=os.path.join(os.path.abspath(os.curdir),'/XBRLData/Summary/')
            # file_path=os.path.join(path,file_name)


            # print(file_path)
            # file_path=os.getcwd()+file_path
            # #重命名
            # os.rename(file_path,os.path.abspath(os.curdir)+'/XBRLData/Summary/' +str(stock_num[num])+'__'+names[0]+'.htm')
            # #复制
            # file_path=os.path.join(path,file_path)
            # file_path=os.getcwd()+file_path
            # shutil.copy(os.path.abspath(os.curdir)+'/XBRLData/Summary/' +str(stock_num[num])+'__'+names[0]+'.htm',WORK_PATH)
            # #删除文件夹
            # shutil.rmtree(os.path.abspath(os.curdir)+'/XBRLData')

if __name__=='__main__':
    get_xbrldata([2702,2703])

