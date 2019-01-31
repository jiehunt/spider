#/usr/bin/env python
#coding=utf8
import hashlib
import urllib
import random
import re
import sys
import time
import datetime
from lxml import html
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import NewPost
# from newspaper import Article
# reload(sys)
# sys.setdefaultencoding('utf-8')
time1 = time.time()
#得到html的源码
def gethtml(url1):
    #伪装浏览器头部
    headers = {
       'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'
    }
    req = urllib2.Request(
    url = url1,
    headers = headers
    )
    html = urllib2.urlopen(req).read()
    return html
#得到目标url源码
# code1 = gethtml('http://whuhan2013.github.io/archive/')

# tree = html.fromstring(code1)
#print tree

# targeturl=tree.xpath("//li[@class='listing-item']/a/@href")

def sends(data):
    # print targeturl
    #u=content1[i][0]

    #链接WordPress，输入xmlrpc链接，后台账号密码
    wp = Client('http://www.stock-t.com/wordpress/xmlrpc.php','jiehunt','yxpbl1982')
    post = WordPressPost()
    post.title = 'MyStockRecommend'
    # post.post_type='test'
    post.content = data
    post.post_status = 'publish'
    #发送到WordPress
    #print 'here3'
    wp.call(NewPost(post))
    time.sleep(3)
    print ('posts updates')

if __name__=='__main__':

    nowtime = time.strftime('%Y%m%d', time.localtime(time.time()))
    filename = str(nowtime) + 'stockinfo.txt'
    filename = "/home/jiehunt/work/task/" + filename
    f = open(filename)
    data1 = f.read()  # ファイル終端まで全て読んだデータを返す
    data2 = re.search( 'Recommend Stock is', data1)
    if data2:
       (a,b) = data2.span()
       data3 = 'Recommend Stock is:' + data1[b+2:]
       sends(data3)

    f.close()
