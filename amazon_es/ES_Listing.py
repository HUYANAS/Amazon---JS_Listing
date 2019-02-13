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

# list = [('产品url','asin','星级','评论数','标题')]
listing_url = []
asin = []
title = []
rate = []
reviews = []
brand = []
n = 1
t_list = []


# 返回url页面的结果，是一个xpath对象
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
        'origin': 'https://www.amazon.es',
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


# 读取文件放入到队列q中
def read_file(n):
    fp = open('a.csv', 'r',encoding='utf-8')
    # fp = codecs.open('a.csv', 'r',encoding='utf-8',errors='ignore')
    w = fp.readlines()
    q = queue.Queue()
    for i in w[n:]:
        u = []
        u.append(i.split(',')[0])
        u.append(i.split(',')[1][:-1])
        q.put(u)
    fp.close()
    return q

#循环读取q中的数据并爬取
# def requ(q,q_test,q_root,mutex):
#     while True:
#         if q.empty():
#             break
#         else:
#             u = q.get()
#             print('正在查找类目：%s' % u[1])
#             selector = response(u[0])
#
#
#
#             # for i in list_a(selector):
#             #     x.append(i)
#             # # 有第二页则返回，没有则跳过
#             # try:
#             #     url2 = selector.xpath('//div[@class="a-text-center"]//li[@class="a-last"]//a/@href')[0]
#             #     selector2 = response(url2)
#             #     for i in list_a(selector2):
#             #         x.append(i)
#             # except Exception as e:
#             #     pass
#     print('列表写入完成')

def get_1(q_test, q_root,mutex,filename):
    while True:
        if q_test.empty():
            break
        else:
            u = q_test.get()
            time.sleep(0.5)
            res = response(u[0])
            goal = res.xpath('//span[contains(text(),"No disponible")]')
            if goal:
                mutex.acquire()
                fp = open(filename,'a',encoding='utf8')
                lis = res.xpath('//ul[@id="s-results-list-atf"]/li[contains(@id,"result")]')
                for i in lis:
                    aim = i.xpath('.//span[contains(text(),"No disponible")]')
                    if aim:
                        # fp = open(filename,'a',encoding='utf8')
                        # listing_url = i.xpath(".//a[contains(@class,'a-link-normal s-access-detail-page')]")[0]
                        asin1 = i.xpath("./@data-asin")
                        if asin1:
                            global n
                            print('找到第%s条,该asin为：%s' % (n,asin1[0]))
                            n += 1
                            listing_url1 = 'https://www.amazon.es/dp/' + asin1[0]
                            asin.append(asin1[0])
                            listing_url.append(listing_url1)
                        else:
                            asin.append('')
                            listing_url.append('')
                        # print(reviews)
                        title1 = i.xpath(".//a[contains(@class,'a-link-normal s-access-detail-page')]/@title")
                        if title1:
                            title.append(title1[0])
                        else:
                            title.append('')
                        rate1 = i.xpath(".//span[@class='a-icon-alt' and contains(text(),'5')]/text()")
                        brand1 = i.xpath(".//div[@class='a-row a-spacing-mini']//span[@class='a-size-small a-color-secondary'][2]/text()")
                        if brand1:
                            brand.append(brand1[0])
                        else:
                            brand.append('')
                        if rate1:
                            rate2 = rate1[0]
                            rate2 = rate2.replace(',','.')
                            rate2 = rate2.split(' ')
                            rate.append(rate2[0])
                            # reviews1 = i.xpath(".//span[contains(@name,%s)]/a[@class='a-size-small a-link-normal a-text-normal']/text()" %asin1[0])
                            reviews1 = i.xpath(".//div[@class='a-row a-spacing-none']//span[@class='a-declarative']/../../a[@class='a-size-small a-link-normal a-text-normal']/text()")
                            if reviews1:
                                g = reviews1[0].replace('.','')
                                reviews.append(g)
                        else:
                            rate.append('')
                            reviews.append('')
                        # print(rate)
                        # print(asin)
                        c = (listing_url[-1], asin[-1],rate[-1], reviews[-1], brand[-1],title[-1])
                        for x in c:
                            # if isinstance(x,str):
                            x = x.lstrip()
                            x = x.rstrip()
                            x = x.replace('…', '...')
                            x = x.replace('&nbsp;', ' ')
                            x = x.replace('\n', '')
                            x = x.replace(',', '，')
                            fp.write(x)
                            fp.write(',')
                        fp.write('\n')
                        # fp.close()
                        # q_root.put((listing_url[-1], asin[-1], title[-1],rate[-1], reviews[-1]))
                    else:
                        continue
                fp.close()
                mutex.release()
    return q_root

def main():
    while True:
        try:
            n = input('从第几个开始抓取（输入大于0的整数）：')
            n = int(n)
            break
        except Exception as e:
            print('输入有误，请重新输入')
            continue
    q = read_file(n)
    a = datetime.date.today()
    filename = '%s年%s月%s日_西班牙无主ASIN采集数据.csv' % (a.year, a.month, a.day)
    # fp = open(filename, 'a', encoding='utf8')

    mutex = threading.Lock()
    q_test = queue.Queue()
    q_root = queue.Queue()
    # q_root.put(('产品url', 'asin', '星级', '评论数', '品牌', '标题'))
    with open(filename, 'a', encoding='utf8') as fp:
        fp.write('产品url, asin, 星级, 评论数, 品牌, 标题\n')
    filename_2 = 'a_used.csv'
    with open(filename_2, 'a', encoding='utf8') as ft:
        ft.write('url,title\n')
    # ft.close()
    # y = 1
    try:
        while True:
            if q.empty():
                break
            else:

                u = q.get()
                e = u[0] + ',' + u[1] + '\n'
                with open(filename_2,'a',encoding='utf8') as fe:
                    fe.write(e)
                print('正在查找类目：%s' % u[1])
                selector = response(u[0])
                page_m = selector.xpath("//span[contains(@class,'pagnDisabled')]/text()")
                print(page_m)
                if page_m:
                    page_n = int(page_m[0])
                else:
                    page_n = 2
                if page_n <= 30:
                    page_n = 201
                    print(page_n)
                for i in range(2,page_n):
                # for i in range(2,201):
                    page_url = u[0] + '&page=' + str(i)
                    page_name = u[1]
                    q_test.put((page_url,page_name))
                # if y == 1:
                for j in range(1,16):
                    t = threading.Thread(target=get_1, args=(q_test, q_root,mutex,filename))
                    # t = threading.Thread(target=get_1, args=(q_test, q_root,mutex,filename))
                    t_list.append(t)
                for c in t_list:
                    c.start()
                    print("%s线程启动" % c)
                    # y += 1
                for d in t_list:
                    d.join()
                t_list.clear()
                # for w in range(1,16):

    finally:
        # fp.close()
        # ft.close()
        pass

    # q_root = queue.Queue()
    # q_test = queue.Queue()
    # mutex = threading.Lock()
    # # 开启10个线程
    # for i in range(1, 11):
    #     t = threading.Thread(target=requ, args=(q, q_test, q_root, mutex))
    #     t.start()
    #     print("第%s个线程启动" % i)
    # # 等待线程
    # for i in range(1, 11):
    #     t.join()

#写入文件
# for i in range(len(list)):
#     for j in range(7):
#         x = list[i][j]
#         if j == 0 or j == 4 or j == 7:
#             x = x.lstrip()
#             x = x.rstrip()
#             x = x.replace('…', '...')
#             x = x.replace('\n','')
#             x = x.replace(',', '，')
#         if j == 2:
#             m = x.split(' ')
#             x = m[0]
#             x = x.replace(',','，')
#         if j == 3:
#             x = x.replace(',', '')
#         if j == 5:
#             if isinstance(x, int):
#                 x = str(x)
#         f.write(x)
#         if j <6:
#             f.write(',')
#     f.write('\n')
# f.close()
# print('写入完成。。。')

if __name__ == '__main__':
    main()