# /usr/bin/env python3
# _*_ coding:utf-8 _*_
# auther: saucerman
# project: https://github.com/saucer-man/penetration-script

"""
decription : 检测网站源码泄露，备份文件泄露
"""

import getopt
import sys
import requests
import queue
import threading
class source_leak_check(threading.Thread):
    def __init__(self, queue, payloads):
        threading.Thread.__init__(self)
        self.queue = queue
        self.payloads = payloads
    def run(self):
        while not self.queue.empty():
            url=self.queue.get()
            headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"}
            for payload in self.payloads:
                vulnurl = url + payload
                try:
                    flag = 0
                    print('\033[1;33m[*]test:  %s\033[0m'%vulnurl)
                    # 如果是备份文件则不需要下载，只需要head方法获取头部信息即可，否则文件较大会浪费大量的时间
                    if 'zip' in payload or 'rar' in payload or 'gz' in payload or 'sql' in payload or 'tore' in vulnurl:
                        req = requests.head(vulnurl, headers=headers, timeout=3, allow_redirects=False)
                        if req.status_code == 200:
                            if 'html' not in req.headers['Content-Type'] :
                                flag = 1
                    # 当检验git和svn、hg时则需要验证返回内容，get方法
                    else:
                        req = requests.get(vulnurl, headers=headers, timeout=3, allow_redirects=False)
                        if req.status_code == 200:
                            if 'svn' in payload:
                                if 'dir' in req.content and 'svn' in req.content:
                                    flag = 1
                            elif 'git' in payload:
                                if 'repository' in req.content:
                                    flag = 1
                            elif 'hg' in payload:
                                if 'hg' in req.content:
                                    flag = 1
                            elif '/WEB-INF/web.xml' in payload:
                                if 'web-app' in req.content:
                                    flag = 1
                    
                    if flag == 1:
                        with open('result.txt', 'a') as f1:
                            f1.write(vulnurl + '\n')
                        print("\033[1;31m[+]信息泄露\tpayload: %s\033[0m"%vulnurl)
                    # else:
                        # print("[-]不存在源码泄露\tpayload: " + vulnurl)
                except:
                    # print("[-]连接失败\tpayload: "+vulnurl)
                    pass

def usage():
    print('----------------------------')
    print('')
    print("SOURCE LEAK DETECTION")
    print("Usage: python source_leak_check.py -u url -l target.txt")
    print("-u --url=baidu.com       --specify a single target ")
    print("-l --list=target.txt     - batch scanning")
    print("Examples: ")
    print("./01.py -u http://xiaogeng.top")
    print("./01.py -l target.txt")
    print('')
    print('----------------------------')
    sys.exit(0)



def main():
    urlList = []
    with open('dictionary.txt') as f:
        payloads = f.read().splitlines()

    if not len(sys.argv[1:]):
        usage()

    # read the parameters
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hl:u:",
                                   ["help", "url=", "list="])
    except :
        usage()
    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
        elif o in ("-u", "--url"):
            if '//' not in a:
                a = 'http://' + a
            urlList.append(a)
        elif o in ("-l", "--list"):
            with open(a, 'r', encoding='utf8')as f:
                urls = f.readlines()
                for tmp in urls:
                    if '//' in tmp:
                        url = tmp.strip('\n')
                    else:
                        url = 'http://' + tmp.strip('\n')
                    urlList.append(url)
            f.close()
        else:
            assert False, "Unhandled Option"
    print('ready Runing:')
    threads = []
    threads_count = 30
    q=queue.Queue()
    for url in urlList:
        q.put(url)
    for i in range(threads_count):
        threads.append(source_leak_check(q,payloads))
    for t in threads:
        t.start()
        t.join()
    print('检测结束，结果已保存至result.txt')
if __name__=="__main__":
    main()

