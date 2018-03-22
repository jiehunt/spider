# -*- coding:utf-8 -*-
import requests
import urllib
import urllib3
import re
import numpy as np
from bs4 import BeautifulSoup
import string
from locale import *
import os, sys
import time
import pandas as pd
# setlocale(LC_NUMERIC, 'English_US')

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

def get_price_list(urlbase):
    try:
        http = urllib3.PoolManager()
        request = http.request('GET', urlbase)
        # response = http.urlopen(request)
        # html = response.read()
    except urllib.URLError as e:
        if hasattr(e, "code"):
            print('error code')
            print (e.code)
        if hasattr(e, "reason"):
            print('error reason')
            print (e.reason)


    soup = BeautifulSoup(request.data, "lxml")
    #prices = soup.find_all("dd",class_="stc-now")
    # prices = soup.find_all("td", class_="stoksPrice")
    prices = soup.find_all("td")

    Sts = []

    for p in prices:
        nStr = ""
        if len(p.contents)  == 1:
            pp = (p.contents[0])
        else:
          continue
        pp = nStr.join(pp)
        Sts.append(pp)

    # for s in Sts:
    #     print (s)
    #     print ("--------")

    fmtcnt = -1
    mysheet = pd.DataFrame(columns=['Date','StartPrice','HighPrice','LowPrice','EndPrice','Count','FinalPrice'])
    mycell = pd.Series(index=['Date','StartPrice','HighPrice','LowPrice','EndPrice','Count','FinalPrice'])
    col = 0

    # StartPrice HighPrice LowPrice EndPrice Count FinalPrice
    for s in Sts:
        # if (str(s).find('年') and str(s).find('月') ):
        if s.endswith(r'日'):
            # mysheet=mysheet.append({"Date": s}, ignore_index=True)
            mycell['Date'] = s
            fmtcnt = 0
            continue
        if fmtcnt == 0:
            #mysheet["StartPrice"] = s
            mycell['StartPrice'] = s
            fmtcnt = 1
            continue
        if fmtcnt == 1:
            mycell['HighPrice'] = s
            fmtcnt = 2
            continue
        if fmtcnt == 2:
            mycell['LowPrice'] = s
            fmtcnt = 3
            continue
        if fmtcnt == 3:
            mycell['EndPrice'] = s
            fmtcnt = 4
            continue
        if fmtcnt == 4:
            mycell['Count'] = s
            fmtcnt = 5
            continue
        if fmtcnt == 5:
            mycell['FinalPrice'] = s
            fmtcnt = 6
            mysheet=mysheet.append(mycell,ignore_index=True)
            continue

    return mysheet



"""
メイン関数
"""
if __name__ == '__main__':
    columns=['Date','StartPrice','HighPrice','LowPrice','EndPrice','Count','FinalPrice']
    m_newhighlist = newhighlist()
    time.localtime(time.time())
    nowtime = time.strftime('%Y%m%d',time.localtime(time.time()))
    filename = nowtime + 'stockinfo.txt'
    file = open(filename, "w")

    cnt = 0
    newhigh = ['2226','2384']
    urlbase = 'http://www.nikkei.com/markets/company/?scode='
    # for item in m_newhighlist.code_num:
    for item in newhigh:
        url = urlbase + item
        print (url)
        # getpriceandjikasougaku(url,item)
        cnt += 1

    mysheet = pd.DataFrame()
    for n in range(1,4):
        # urlbase = 'https://stocks.finance.yahoo.co.jp/stocks/history/?code=6083.T'
        urlbase = 'https://info.finance.yahoo.co.jp/history/?code=6083.T'
        urlbase = urlbase + '&p=' + str(n)
        newsheet = get_price_list(urlbase)
        if n > 0:
          mysheet = pd.concat((mysheet, newsheet))
        else:
          mysheet = newsheet

    mysheet = mysheet.reset_index(drop=True)

    mysheet['updown_today'] = mysheet['EndPrice'] > mysheet['StartPrice']
    mysheet['updown_yestoday'] = 0.0
    for name in ['StartPrice','HighPrice','LowPrice','EndPrice','Count','FinalPrice']:
        mysheet[name] = mysheet[name].apply(lambda x: int(x.replace(',', '')))

    print ( "*************")
    for index , row in mysheet.iterrows():
        if index < mysheet.shape[0] -1 :
            next_row = mysheet.loc[[index+1]]
            mysheet.set_value(index, 'updown_yestoday',  row['StartPrice'] - next_row['FinalPrice'].values)


    print (mysheet)
    """
    file.write ("Recommend Stock is :")
    file.write ("\n")
    for item in m_newhighlist.code_num:
        index = m_newhighlist.code_num.index(item)
        if (m_newhighlist.stockinfo_list[index].keijyou_value > 2) and \
            m_newhighlist.stockinfo_list[index].towyear_high == 1 and \
            m_newhighlist.stockinfo_list[index].sougaku_value > 30000 :
            file.write (item)
            file.write ("\n")
    """

    file.close()
