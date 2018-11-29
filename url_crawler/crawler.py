# /usr/bin/env python3
# _*_ coding:utf-8 _*_
# auther: saucerman
# project: https://github.com/saucer-man/UrlCrawler

"""
decription : 全站url爬取脚本
"""
import re
import time
import sys
import requests
try :
    import tldextract
except:
    print('module tldextract not fount \nyou can try pip install tldextract')
    sys.exit()


def domain_get():
    '''
    接收要爬取的网站url
    '''
    url = input("Please input the url of website:")
    if '//' not in url:
        url = 'http://' + url
    try:
        kv={'user_agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}
        requests.head(url,headers=kv)
        return url
    except:
        print("your url is incorrect!!")
        return domain_get()


class spider():
    def __init__(self, domain, key, depth):
        self.domain = domain # 爬取的域名
        self.depth = depth # 爬取的深度
        self.urls_all = set([]) # 爬取的结果
        self.key = key # 顶级域名，用于排除外链

    def page_spider(self, url):
        '''
        爬取url中的所有链接
        '''
        try:
            kv={'user_agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}
            r = requests.get(url, headers=kv, timeout = 2)
            r.encoding=r.apparent_encoding
            pagetext=r.text
            pagelinks = re.findall(r'(?<=href=\").*?(?=\")|(?<=href=\').*?(?=\')',pagetext)
            
        except:
            return set([])
        # 接下来对爬取的链接进行处理

        # 1、先去除不同域的链接
        url_list = set([])
        for url in pagelinks:
            if self.key in url:
                url_list.add(url)

        # 2、再对链接进行去重处理
        url_list = set(url_list)-self.urls_all 
        self.urls_all.update(url_list) 
        return url_list  # 返回集合



    def run(self):
        url_list = set([self.domain]) # 第一次爬取原始url的链接
        while self.depth >= 1: # 每一次深度的爬取都会爬取url_list的所有链接
            print("倒数第%d轮"%self.depth)
            url_list_tmp = set([])
            for url in url_list:
                url_list_tmp.update(self.page_spider(url))
            url_list = url_list_tmp
            self.depth = self.depth -1
        
        file=open('result.txt','w')
        for url in self.urls_all:
            file.write(url)
            file.write('\n')
        file.close()




if __name__ == '__main__':
    time.clock()
    domain = domain_get()
    print('domain:', domain)
    key_tmp  = tldextract.extract(domain)
    # 用于排除外链，爬取的url不包含key的都会被舍弃。
    # 'https://www.xiaogeng.com.cn/admin?id=6'==>'www.xiaogeng.com.cn'
    key = key_tmp.subdomain + '.' + key_tmp.domain+'.' + key_tmp.suffix 
    print('key:', key)
    print('开始爬取...\n')
    spider = spider(domain = domain, key = key, depth = 3)
    spider.run()
    print('结果已保存至result.txt中')
    print('time:',time.clock())


