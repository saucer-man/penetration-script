#!/usr/bin/python3
# -*- coding: utf-8 -*-


import ssl
import time
import warnings

import requests
from bs4 import BeautifulSoup

warnings.filterwarnings("ignore")
ssl._create_default_https_context = ssl._create_unverified_context

headers = {
    'Host': 'www.butian.net',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'close',
    'Referer': 'https://www.butian.net/Reward/plan/2',
    'Cookie': '这里填入cookie',
    'Upgrade-Insecure-Requests': '1',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache'
}


def parse_page(data):
    datas = data['data']['list']
    for d in datas:
        # 获取厂商url
        url = "https://www.butian.net/Loo/submit?cid=" + d['company_id']
        website = parse_submit(url)
        save(url + "  " + d['company_name'] + "  " + website)
        time.sleep(1)


def parse_submit(url):
    try:
        # 获取厂商url
        webdata = requests.get(url=url, headers=headers)
        webdata.encoding = webdata.apparent_encoding
        soup = BeautifulSoup(webdata.text, 'html.parser')
        website = soup.find_all('input', class_='input-xlarge')[1]['value']
        return website
    except Exception as e:
        print(f"爬取{url}错误: {e}")
        time.sleep(10)
        return parse_submit(url)


def save(msg):
    with open("result.txt", "a") as f:
        f.write(msg)
        f.write("\n")


def get_end_page():
    """
    看一下总共有多少页
    :return: int
    """
    url = 'https://www.butian.net/Reward/pub'
    data = {
        's': 1,
        'p': 1
    }
    r = requests.post(url=url, data=data)
    return int(r.json()["data"]["count"])


def main():
    end_page = get_end_page()
    for i in range(1, end_page + 1):
        print(f'目前获取第 {i} 页')
        url = 'https://www.butian.net/Reward/pub'
        data = {
            's': 1,
            'p': i
        }
        r = requests.post(url=url, data=data)
        parse_page(r.json())
        time.sleep(3)


if __name__ == '__main__':
    main()
    print("补天公益SRC厂商URL获取结束...")
