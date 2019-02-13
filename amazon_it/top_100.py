# _*_ coding:utf-8 _*_

import requests
from lxml import etree
import random
import queue
import threading

#初始化选项
title = []
rate = []
price = []
reviews = []
rank = []
link = []
list = [('title','price','rate','reviews','mu','rank','link')]

# 返回url页面的结果，是一个xpath对象
def response(url):
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
    ]
    headers = {
        'User-Agent': random.choice(USER_AGENTS_LIST),
    }
    answer = requests.get(url, headers=headers)
    res = etree.HTML(answer.text)
    return res

# 返回每个链接里面每一项li标签
def list_a(selector):
    a = []  #用来存放每一页的lis
    for i in selector.xpath('//li[@class="zg-item-immersion"]'):
        a.append(i)
    return a

#返回每一个产品的详细信息到list
def b(a,m,mutex):
    # 锁定
    mutex.acquire()
    for i in a:
        title1 = i.xpath(".//div[contains(@class,'p13n-sc-truncate')]/text()") #获取标题
        if title1:
            title.append(title1[0])
        else:
            title.append('')
        rate1 = i.xpath('.//span[@class="a-icon-alt"]/text()')  #获取星级
        if rate1:
            rate.append(rate1[0])
        else:
            rate.append('')
        price1 = i.xpath('.//span[@class="p13n-sc-price"]/text()')  #获取价格
        if price1:
            price.append(price1[0])
        else:
            price.append('')
        reviews1 = i.xpath('.//a[@class="a-size-small a-link-normal"]/text()')  #获取评价数
        if reviews1:
            reviews.append(reviews1[0])
        else:
            reviews.append('')
        rank1 = i.xpath('.//span[@class="zg-badge-text"]/text()')  # 获取排名
        if rank1:
            rank.append(rank1[0])
        else:
            rank.append('')
        link1 = i.xpath('.//a[@class="a-link-normal"]/@href')  #获取链接
        if link1:
            link2 = 'https://www.amazon.co.uk' + link1[0]
            link.append(link2)
        else:
            link.append('')
        list.append((title[-1],price[-1],rate[-1],reviews[-1],m,rank1[-1],link[-1]))
    # 释放
    mutex.release()
    return list

# 读取文件并放入到队列q中
def read_file():
    fp = open('a.csv', 'r',encoding='utf-8')
    w = fp.readlines()
    q = queue.Queue()
    for i in w[1:]:
        u = []
        u.append(i.split(',')[0])
        u.append(i.split(',')[1][:-2])
        q.put(u)
    return q

#循环读取q中的数据并爬取
def requ(q,mutex):
    while True:
        if q.empty():
            break
        else:
            u = q.get()
            x = []
            selector = response(u[0])
            print('开始写入列表。。。')
            for i in list_a(selector):
                x.append(i)
            print(u[0])
            # 有第二页则返回，没有则跳过
            try:
                url2 = selector.xpath('//div[@class="a-text-center"]//li[@class="a-last"]//a/@href')[0]
                selector2 = response(url2)
                for i in list_a(selector2):
                    x.append(i)
            except Exception as e:
                pass
            b(x,u[1],mutex)
    print('列表写入完成')

def main():
    q = read_file()
    mutex = threading.Lock()
    #开启10个线程
    for i in range(1,11):
        t = threading.Thread(target=requ, args=(q,mutex))
        t.start()
        print("第%s个线程启动" % i)
    # 等待线程
    for i in range(1,11):
        t.join()
    #写入文件
    filename = input('输入要保存的文件名：')
    filename = filename + '.csv'
    print('写入文件中。。。')
    f = open(filename,'a',encoding='utf-8')
    for i in range(len(list)):
        for j in range(7):
            x = list[i][j]
            if j == 0 or j == 4 or j == 7:
                x = x.lstrip()
                x = x.rstrip()
                x = x.replace('…', '...')
                x = x.replace('\n','')
                x = x.replace(',', '，')
            if j == 2:
                m = x.split(' ')
                x = m[0]
                x = x.replace(',','，')
            if j == 3:
                x = x.replace(',', '')
            if j == 5:
                if isinstance(x, int):
                    x = str(x)
            f.write(x)
            if j <6:
                f.write(',')
        f.write('\n')
    f.close()
    print('写入完成。。。')

if __name__ == '__main__':
    main()
