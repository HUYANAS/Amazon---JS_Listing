# _*_ coding:utf-8 _*_
import requests
from lxml import etree
import random
import queue
import threading
import time
import datetime
from fake_useragent import UserAgent
import codecs

fp = codecs.open('b.csv','r',encoding='utf-8',errors='ignore')
w = fp.readlines()
q = queue.Queue()
for i in w[1:]:
    u = []
    u.append(i.split(',')[0])
    u.append(i.split(',')[1][:-1])
    q.put(u)

def response(url):
    ua = UserAgent()
    USER_AGENTS_LIST = [
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
        "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
        "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
        "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
        "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
        "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
        "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
        "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
        'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
        'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',

    ]
    headers = {
        'accept': 'text / html, application / xhtml + xml, application / xml;q = 0.9, image / webp, image / apng, * / *;q = 0.8',
        'accept - language': 'zh - CN, zh;q = 0.9, en;q = 0.8',
        'origin': 'https://www.amazon.it',
        # 'User-Agent': random.choice(USER_AGENTS_LIST),
        'User-Agent': ua.random,
    }
    session = requests.Session()
    session.headers = headers
    answer = session.get(url)
    # answer = requests.get(url, headers=headers)
    res = etree.HTML(answer.text)
    # print(answer.text)
    return res

def get_1(mutex):
    while True:
        if not q.empty():
            u = q.get()
            res = response(u[0])
            mutex.acquire()
            lis = res.xpath("//ul[@class='a-unordered-list a-nostyle a-vertical a-spacing-base'][1]/li//text()")
            print(lis)
            a = ''
            for x in lis:
                x = x.lstrip()
                x = x.rstrip()
                x = x.replace('…', '...')
                x = x.replace('&nbsp;', ' ')
                x = x.replace('\n', '')
                x = x.replace(',', '，')
                a += (x+'/')

            with open('f.csv','a+',encoding='utf8') as ft:
                ft.write(u[0] + ',' + a + '\n')
            mutex.release()
        else:
            break

mutex = threading.Lock()
try:
    t_list = []
    for j in range(1, 20):
        t = threading.Thread(target=get_1, args=(mutex,))
        t_list.append(t)
    for c in t_list:
        c.start()
        print("%s线程启动" % c)
        # y += 1
    for d in t_list:
        d.join()
    fp.close()
except:
    pass