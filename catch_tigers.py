# -*- coding: utf-8 -*-
import requests
import time
from bs4 import BeautifulSoup

def getTigersUpdate():
    tigers_update_url = 'http://www.ccdi.gov.cn/scdc/'
    page = requests.get(tigers_update_url)
    soup = BeautifulSoup(page.content,from_encoding='utf-8')
    # 获取所有老虎的信息
    content_list=[]
    url_list=[]
    # http://www.ccdi.gov.cn/scdc/zggb/zjsc/201905/t20190520_194211.html
    # http://www.ccdi.gov.cn/scdc/ + ./zggb/zjsc/201905/t20190520_194211.html
    for item in soup.select('.list_news_dl.fixed li a'):

        content_list.append(item.string)

        url = 'http://www.ccdi.gov.cn/scdc'+item['href'][1:]
        url_list.append(url)
    return content_list,url_list

def getTigersUpdate_from_local():
    soup = BeautifulSoup(open("tigers.htm"))
    # 获取所有老虎的信息
    content_list=[]
    url_list=[]
    # http://www.ccdi.gov.cn/scdc/zggb/zjsc/201905/t20190520_194211.html
    # http://www.ccdi.gov.cn/scdc/ + ./zggb/zjsc/201905/t20190520_194211.html
    for item in soup.select('.list_news_dl.fixed li a'):

        content_list.append(item.string)

        # url = 'http://www.ccdi.gov.cn/scdc'+item['href'][1:]
        url_list.append(item['href'])
    return content_list,url_list

def sendMsg(content,url):
    txt='**又有老虎被抓啦！**'  # 标题
    desp = content +', 网页链接：'+ url
    payload = {'text':txt,'desp':desp}
    requests.get('http://sc.ftqq.com/SCU49006T9c252f5cbd9cb04f67d9adc79489c40b5cb5ea43f2163.send', params = payload)
 
if __name__ == '__main__':
    content,urls = getTigersUpdate()
    while True:
        print (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        content_new ,urls_new = getTigersUpdate()
        i = 0
        for (t1,t2) in zip(content,content_new):
            if t1 != t2:
                print("新老虎："+t2)
                sendMsg(t2,urls_new[i])
                # 更新老虎和链接
                content,urls = content_new,urls_new
            i = i + 1            
        time.sleep(60*5)