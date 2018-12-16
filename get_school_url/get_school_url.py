# /usr/bin/env python3
# _*_ coding:utf-8 _*_
# auther: saucerman
# project: https://github.com/saucer-man/penetration-script

"""
基于 http://www.hao123.com/edu 获取高校url

环境：
    pip install BeautifulSoup
    pip install lxml
    pip install tldextract

用法：
python get_school_url.py school.txt
"""

import requests,sys
from bs4 import BeautifulSoup
import tldextract

url = 'http://www.hao123.com/edu'
headers = {
    'Host': 'www.hao123.com',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0',
    'Referer': 'http://www.hao123.com/exam/wangzhi',
}
area_url_list = []
school_url = []

def get_area_url_list():
    global area_url_list
    try:
        response = requests.get(url=url,headers=headers)
    except Exception as e:
        print(e)
        sys.exit()
    soup = BeautifulSoup(response.text,"lxml")
    div = soup.select("[href^='http://www.hao123.com/eduhtm']")
    for tag in div[1:-2]:
        area_url = tag.get('href')
        area_url_list.append(area_url)

def get_school_url():
    global school_url
    for area_url in area_url_list:
        try:
            response = requests.get(url=area_url, headers=headers,timeout=3)
        except:
            continue
        soup = BeautifulSoup(response.text, "lxml")
        div = soup.select("a[href^=http://]")
        for tag in div[60:-5]:
            target_url = str(tag.get('href'))
            school_url.append(target_url)


def filter_school_url():
    global school_url
    tmplist = []
    for url in school_url:
        if 'baike' not in url:
            ext = tldextract.extract(url)
            tmplist.append('http://' + '.'.join(ext[0:3]))
    school_url = tmplist


def save_school_url(filename):
    count = 0
    with open(filename,'w') as f:
        for url in school_url:
            f.writelines(url+'\n')
            count += 1

if __name__ =="__main__":
    try:
        filename = sys.argv[1]
    except:
        filename = 'school.txt'
    get_area_url_list()
    get_school_url()
    filter_school_url()
    save_school_url(filename)
    print("Totle: %d" % len(school_url))
    print("Saved in %s"%filename)
