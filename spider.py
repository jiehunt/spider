# -*- coding: utf-8 -*-
import requests
import urllib
import urllib3
import urllib.request
import re
from bs4 import BeautifulSoup
import string
from locale import *
import os, sys
import time
# setlocale(LC_NUMERIC, 'English_US')

#reload(sys)
#sys.setdefaultencoding('utf-8')

class code_info:

    def __init__(self,num):
        self.code_num = num;
        self.pricenow = 0
        self.uri_list = []
        self.eigyou_list = []
        self.keijyou_list = []
        self.touki_list = []
        self.towyear_high = 0
        self.keijyou_value = 0
        self.sougaku = ""
        self.sougaku_value = 0


class newhighlist:
    def __init__(self):
        self.code_num = []
        self.code_name = []
        self.stockinfo_list = []


"""
新高値につけた銘柄の収集
"""
def getnewhighprice(url):

    try:
        http = urllib3.PoolManager()
        request = http.request('GET', url)
        # request = urllib.Request(url)
        # response = urllib3.urlopen(request)
        # html = response.read()
    except (urllib.URLError, e):
        if hasattr(e, "code"):
            print('error code')
            print (e.code)
        if hasattr(e, "reason"):
            print('error reason')
            print (e.reason)

    soup = BeautifulSoup(request.data, "lxml")
    # soup = BeautifulSoup(html, "lxml")
    headers = soup.find_all("th")
    details = soup.find_all("td")

    for header in headers:
        # file.write (header.string.encode('utf-8')),
        file.write (header.string),
        file.write (";"),
    file.write ("\n")

    for num in range(len(details)//6):
        for i_num in range(len(headers)):
            if not (details[i_num + num*len(headers)].string):
                file.write (" "),
            else:
                # file.write (details[i_num + num*len(headers)].string.encode('utf-8')),
                file.write (details[i_num + num*len(headers)].string),
                file.write (";"),
            if (i_num + num*len(headers)) % 6 == 0 :
                m_newhighlist.code_num.append(details[i_num + num*len(headers)].string)
            elif (i_num + num*len(headers)) % 6 == 1 :
                m_newhighlist.code_name.append(details[i_num + num*len(headers)].string)
        file.write ("\n")

    return

"""
業績などのListから増減率の算出
・　（今期-前期）/前期
"""
def getpersent(list):
    reslist = []
    for num in range(1,len(list)):
        if (list[num-1] == 0):
            file.write ('%.2f%%'%0),
            reslist.append(0);
        else:
            file.write ('%.2f%%' %(((list[num] - list[num-1])/list[num-1])*100)),
            reslist.append( (list[num] - list[num-1])/list[num-1]*100 )
        if num < (len(list)-1):
            file.write (";"),

    if ( reslist[-1] > 0.2) and ( reslist[-2] > 0.2):
        res = 4
    elif ( reslist[-1] > 0.1) and ( reslist[-2] > 0.1):
        res = 3
    elif ( reslist[-1] > 0) and ( reslist[-2] > 0):
        res = 2
    else :
        res = 1

    return res

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False

"""
StringからFlaotへの変換
・　特殊符号は出る場合は、0を返す
"""
def convertstrings(str0):
    res = 0.0
    pattern = re.compile('(^\D)(.*)$')
    m = re.match(pattern,str0)
    if  (m):
        #print(str0)
        if len(m.group(2)) == 0:
            res = 0
        else:

            #test = m.group(2).encode('ascii','ignore')
            test = m.group(2)
            #print(test)
            if is_number(test):
                res = -atof(m.group(2))
            else:
                res = 0
    else :
        str0 = str0.replace(",", "")
        res = atof(str0)

    return res

"""
業績などの情報の抽出
"""
def getgyouseki(url,code):
    try:
        http = urllib3.PoolManager()
        request = http.request('GET', url)
        # request = urllib3.Request(url)
        # response = urllib3.urlopen(request)
        # html = response.read()
    except (urllib.URLError, e):
        if hasattr(e, "code"):
            print('error code')
            print (e.code)
        if hasattr(e, "reason"):
            print('error reason')
            print (e.reason)

    soup = BeautifulSoup(request.data, "lxml")
    # soup = BeautifulSoup(html, "lxml")
    headers = soup.find_all("th")
    details = soup.find_all("td")

    index = m_newhighlist.code_num.index(code)

    for num in range(5,10):
        m_newhighlist.stockinfo_list[index].uri_list.append( convertstrings(details[num].string) )

    for num in range(10,15):
        m_newhighlist.stockinfo_list[index].eigyou_list.append( convertstrings(details[num].string) )

    for num in range(15,20):
        m_newhighlist.stockinfo_list[index].keijyou_list.append( convertstrings(details[num].string) )

    for num in range(20,25):
        m_newhighlist.stockinfo_list[index].touki_list.append( convertstrings(details[num].string) )

    cnt = 0
    res = 0
    limit = 7 #the size of header
    for header in headers:
        if not ("colspan" in header.attrs):
            for child in header.descendants:
                # file.write (child.encode('utf-8')),
                file.write (child),
                file.write (";"),
                break

            for num in range(5):
                s = details[num+cnt*5].string
                if s:
                    # file.write(s.encode('utf8'))
                    file.write(s)
                else :
                    file.write("0")
                #file.write (details[num+cnt*5].string.encode('utf-8')),
                file.write (";"),
            if cnt == 1:
                getpersent(m_newhighlist.stockinfo_list[index].uri_list)
            elif cnt == 2:
                getpersent(m_newhighlist.stockinfo_list[index].eigyou_list)
            elif cnt == 3:
                res = getpersent(m_newhighlist.stockinfo_list[index].keijyou_list)
                m_newhighlist.stockinfo_list[index].keijyou_value = res
                if res == 4:
                    file.write (";"),
                    file.write (r"◎"),
                elif res == 3:
                    file.write (";"),
                    file.write (r"○"),
                elif res == 2:
                    file.write (";"),
                    file.write (r"▲"),
                elif res == 1:
                    file.write (";"),
                    file.write (r"×"),
            elif cnt == 4:
                getpersent(m_newhighlist.stockinfo_list[index].touki_list)

            cnt += 1
            file.write("\n")
        if cnt > limit:
            break

    file.write ("\n")

    return

"""
指定された銘柄の10間株価の抽出
"""
def get10yearprice(url,code):

    try:
        http = urllib3.PoolManager()
        request = http.request('GET', url)
        # request = urllib3.Request(url)
        # response = urllib3.urlopen(request)
        # html = response.read()
    except (urllib.URLError, e):
        if hasattr(e, "code"):
            print('error code')
            print (e.code)
        if hasattr(e, "reason"):
            print('error reason')
            print (e.reason)

    # soup = BeautifulSoup(html, "lxml")
    soup = BeautifulSoup(request.data, "lxml")
    headers = soup.find_all("th")
    details = soup.find_all("td")

    res = 0

    index = m_newhighlist.code_num.index(code)

    years = []
    pattern = re.compile('200|201')
    for header in headers:
        if (header.string):
            m = re.match(pattern, header.string.strip())
            if (m) :
                years.append( header.string.strip().encode('utf-8') )

    price = []
    cnt = 0
    skip_num = 9 # before year is month
    pattern = re.compile('(^\s)')
    for detail in details:
        for child in detail.children:
            if (child.string):
                if (re.match(pattern, child.string)):
                    if (cnt > skip_num):
                        price.append(convertstrings(child.string))
                    cnt += 1

    if (len(price) > 10):
        if (price[3] > price[1]*0.9) and (price[3] > price[6]*0.9):
            res = 1
            file.write (r"○")
            file.write("\n")
        else:
            file.write (r"×")
            file.write("\n")
    else:
        file.write (r"×")
        file.write("\n")

    for num in range(8,14):
        # file.write (headers[num].string.strip().encode('utf-8')),
        file.write (headers[num].string.strip()),
        if (num < 13):
            file.write (";"),
    file.write ("\n")

    cnt = 0
    for item in years:
        file.write (item.decode('utf-8')),
        file.write (";"),
        for num in range(5):
            file.write (str(price[num + cnt*5])),
            if num < 4:
                file.write (";"),
        cnt += 1
        file.write ("\n")

    m_newhighlist.stockinfo_list[index].towyear_high = res;

    return

def changetoprice(prices):
    if prices.find(','):
        cnt = prices.count(',')
        if (cnt > 4):
            prices = 10000000000000000
        elif (cnt == 3):
            prices = float( prices.split(',')[0]) *1000 * 1000 * 1000 + float( prices.split(',')[1]) *1000 * 1000 + float( prices.split(',')[2]) * 1000 + float( prices.split(',')[3])
        elif (cnt == 2):
            prices = float( prices.split(',')[0]) *1000 * 1000 + float( prices.split(',')[1]) *1000 + float( prices.split(',')[2])
        elif (cnt == 1):
            prices = float(prices.split(',')[0]) * 1000  + float( prices.split(',')[1] )
    else:
        prices = float(prices)

    return prices


"""
株価と時価総額の情報の抽出
"""
def getpriceandjikasougaku(url,code):

    try:
        http = urllib3.PoolManager()
        request = http.request('GET', url)
        # request = urllib3.Request(url)
        # response = urllib3.urlopen(request)
        # html = response.read()
    except (urllib.URLError, e):
        if hasattr(e, "code"):
            print('error code')
            print (e.code)
        if hasattr(e, "reason"):
            print('error reason')
            print (e.reason)

    # soup = BeautifulSoup(html, "lxml")
    soup = BeautifulSoup(request.data, "lxml")
    #prices = soup.find_all("dd",class_="stc-now")
    prices = soup.find("dd",class_="m-stockPriceElm_value now")
    #sougakus = soup.find_all("dd", class_="m-st-top_basic_price_num")
    sougakus = soup.find_all("span", class_="m-stockInfo_detail_value")
    res = 0

    index = m_newhighlist.code_num.index(code)

    nStr = ""
    prices = (prices.contents[0])
    prices = nStr.join(prices)
    prices = changetoprice(prices)
    m_newhighlist.stockinfo_list[index].pricenow = prices

    for sougaku in sougakus:
        nStr = ""
        sougaku = nStr.join(sougaku.get_text())
        if (sougaku.endswith((u"万円"))):
            sougaku =  sougaku.split(' ')[0]
            sougaku = changetoprice(sougaku)
            m_newhighlist.stockinfo_list[index].sougaku_value = sougaku
            #m_newhighlist.stockinfo_list[index].sougaku_value = atoi(m.group(1))

    return

"""
メイン関数
"""
m_newhighlist = newhighlist()
time.localtime(time.time())
nowtime = time.strftime('%Y%m%d',time.localtime(time.time()))
filename = nowtime + 'stockinfo.txt'
file = open(filename, "w")

"""
新高値つけた銘柄の収集
"""
urlbase = 'http://www.morningstar.co.jp/RankingWeb/MarketHighPrice.do?market='
for mkt in range(1,4):
    url = urlbase +str(mkt)
    newhigh = getnewhighprice(url)

for item in m_newhighlist.code_num:
    tmp = code_info(item)
    m_newhighlist.stockinfo_list.append(tmp)

file.write("\n")
#newhigh = ['2226','2384']
"""
指定銘柄の売上、利益などの抽出
"""
urlbase = 'http://www.nikkei.com/markets/company/kessan/shihyo.aspx?scode='
cnt = 0
for item in m_newhighlist.code_num:
    url = urlbase + item
    file.write (url)
    file.write ("\n")
    # file.write (m_newhighlist.code_name[cnt].encode('utf-8'))
    file.write (m_newhighlist.code_name[cnt])
    getgyouseki(url,item)
    cnt += 1

"""
指定銘柄の10年株価などの抽出
"""
cnt = 0
#newhigh = ['2226','2384']
urlbase = 'http://www.nikkei.com/markets/company/history/yprice/?scode='
for item in m_newhighlist.code_num:
    url = urlbase + item
    file.write (url)
    file.write ("\n")
    # file.write ((m_newhighlist.code_name[cnt].encode('utf-8'))),
    file.write ((m_newhighlist.code_name[cnt])),
    file.write (";"),
    get10yearprice(url,item)
    cnt += 1
    file.write ("\n")

"""
指定銘柄の時価総額と株価の抽出
"""
cnt = 0
#newhigh = ['2226','2384']
urlbase = 'http://www.nikkei.com/markets/company/?scode='
for item in m_newhighlist.code_num:
    url = urlbase + item
    #print (url)
    getpriceandjikasougaku(url,item)
    cnt += 1

file.write ("Recommend Stock is :")
file.write ("\n")
for item in m_newhighlist.code_num:
    index = m_newhighlist.code_num.index(item)
    if (m_newhighlist.stockinfo_list[index].keijyou_value > 2) and \
        m_newhighlist.stockinfo_list[index].towyear_high == 1 and \
        m_newhighlist.stockinfo_list[index].sougaku_value > 30000 :
        file.write (item)
        file.write ("\n")

file.close()
