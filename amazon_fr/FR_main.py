# _*_ coding:utf-8 _*_
import requests
import queue
import random
from lxml import etree
import threading
from fake_useragent import UserAgent


def find(m,que_root,que_1):
    res = response(m[0])
    lis = res.xpath("//ul[@class='a-unordered-list a-nostyle a-vertical a-spacing-base'][1]/ul[1]//li")
    # ul = res.xpath("//span[@class='zg_selected']/../following-sibling::ul[1]/li")
    if lis:
        for i in lis:
            w = list()
            au1 = 'https://www.amazon.fr' + i.xpath(".//a/@href")[0]
            w.append(au1)
            w.append(m[1] + '/' + i.xpath(".//span[contains(@class,'a-size-small')]/text()")[0])
            que_1.put(w)
    else:
        que_root.put(m)
        print(m)
    return que_root

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

    ]
    headers = {
        'accept': 'text / html, application / xhtml + xml, application / xml;q = 0.9, image / webp, image / apng, * / *;q = 0.8',
        'accept - language': 'zh - CN, zh;q = 0.9, en;q = 0.8',
        'origin': 'https://www.amazon.de',
        # 'User-Agent': random.choice(USER_AGENTS_LIST),
        'User-Agent': ua.random,
        'Referer': 'https: // www.amazon.de / s / ref = sr_ex_n_1?rh = n % 3A562066 % 2Cp_36 % 3A0 - 20000 % 2Cp_n_availability % 3A419126031 & bbn = 562066 & ie = UTF8 & qid =%E3%80%81',
    }
    # print(ua.random)
    session = requests.Session()
    session.headers = headers
    answer = session.get(url)
    res = etree.HTML(answer.text)
    # print(answer.text)
    return res

def index(url,que_root,que_1):
    res = response(url)
    # ul = res.xpath("//span[@class='zg_selected']/../following-sibling::ul[1]")
    # lis = res.xpath("//ul[@class='a-unordered-list a-nostyle a-vertical a-spacing-base'][1]/li/following-sibling::ul[1]/li")
    lis = res.xpath("//ul[@class='a-unordered-list a-nostyle a-vertical a-spacing-base'][1]/ul[1]//li")
    if lis:
        for li in lis:
            au1 = 'https://www.amazon.fr' + li.xpath(".//a/@href")[0]
            at0 = li.xpath(".//span[contains(@class,'a-size-small')]/text()")[0]
            at1 = 'High-Tech' + '/' + at0
            # at1 = 'Elektronik & Foto/Kamera & Foto/Zubehör/Objektivzubehör' + '/' + at0
            if at0 == 'Garanties':
                continue
            que_1.put([au1,at1])
        return que_1

def get_1(que_1,que_root):
    while True:
        if not que_1.empty():
            m = que_1.get()
            que_root = find(m,que_root,que_1)
        else:
            break
    return que_root


def main():
    a = [('url','title'),]
    b = []
    url = 'https://www.amazon.fr/s/ref=lp_13921051_nr_p_n_availability_1?rh=n%3A13921051%2Cp_n_availability%3A437882031&bbn=13921051&ie=UTF8&qid='
    # url = 'https://www.amazon.de/gp/search/ref=sr_nr_n_17?fst=as%3Aoff&rh=n%3A562066%2Cp_36%3A0-20000%2Cp_n_availability%3A419126031%2Cn%3A%21569604%2Cn%3A571860%2Cn%3A331964031%2Cn%3A392133011&bbn=331964031&ie=UTF8&qid=1545206295&rnid=331964031'
    # url = 'https://www.amazon.it/s/ref=sr_pg_1?rh=n%3A412609031%2Cp_n_availability%3A490214031&bbn=412609031&ie=UTF8&qid='
    global que_root,que_1
    que_root = queue.Queue()
    que_1= queue.Queue()
    que_1 = index(url,que_root,que_1)
    # que_root = get_1(que_1,que_root)
    u = que_1.qsize()
    print(u)
    for i in range(1,u+1):
        t = threading.Thread(target=get_1,args=(que_1,que_root))
        b.append(t)
    for j in b:
        j.start()
        print("%s线程启动"%j)

    for i in b:
        i.join()
    f = open('c.csv','a+',encoding='utf-8')
    while True:
        if que_root.empty():
            break
        else:
            o = que_root.get()
            a.append(o)
    for i in a:
        for j in range(2):
            if j == 0:
                f.write(i[0])
                f.write(',')
            else:
                x = i[1]
                x = x.replace(',', '，')
                f.write(x)
                f.write('\n')
    f.close()

if __name__ == "__main__":
    main()
