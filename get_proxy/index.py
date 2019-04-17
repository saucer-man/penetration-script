#!/usr/bin/env python3
# coding:utf-8
# date:2019/04/17
# 免费代理爬取

from gevent import monkey
monkey.patch_all()
import gevent
import requests
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/8.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36'
}


class GetProxy:
    def __init__(self):
        self.ip_https_list_tmp = set() 
        self.ip_http_list_tmp = set() 
        self.ip_https_list = set() # 筛选之后的https代理
        self.ip_http_list = set() # 筛选之后的http的代理
    def get(self):
        self._xicidaili(5)
        gevent.joinall([gevent.spawn(self._check) for i in range(0, 100)])

    def _xicidaili(self, pages=5):
        # 西刺免费代理IP https://www.xicidaili.com
        for page in range(0, pages):
            url = "https://www.xicidaili.com/nt/{}".format(page)
            r = requests.get(url, headers=headers)
            soup = BeautifulSoup(r.text, 'lxml')
            trs = soup.find_all('tr')
            for i in range(1,len(trs)):
                tr = trs[i]
                tds = tr.find_all("td")
                ip_item = tds[5].text.lower() + "://" + tds[1].text + ":" + tds[2].text
                if ip_item[:5] == "https":
                    self.ip_https_list_tmp.add(ip_item)
                elif ip_item[:4] == "http":
                    self.ip_http_list_tmp.add(ip_item)
    
    def _check(self):
        # 用百度验证https代理
        while len(self.ip_https_list_tmp)>0:
            ip_for_test = self.ip_https_list_tmp.pop()
            proxies = {
            'https': ip_for_test
            }
            try:
                response = requests.get('https://www.baidu.com', headers=headers, proxies=proxies, timeout=3)
                if response.status_code == 200:
                   self.ip_https_list.add(ip_for_test)
            except:
                continue
        # 验证http代理
        while len(self.ip_http_list_tmp)>0:
            ip_for_test = self.ip_http_list_tmp.pop()
            proxies = {
            'http': ip_for_test
            }
            try:
                response = requests.get('http://httpbin.org/ip', headers=headers, proxies=proxies, timeout=3)
                if response.status_code == 200:
                    self.ip_http_list.add(ip_for_test)
            except:
                continue

if __name__ == "__main__":
    Proxy = GetProxy()
    Proxy.get()
    print("https代理：")
    print(Proxy.ip_https_list)
    print("http代理：")
    print(Proxy.ip_http_list)

