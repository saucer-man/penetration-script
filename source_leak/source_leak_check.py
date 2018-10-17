# /usr/bin/env python3
# _*_ coding:utf-8 _*_
# auther: saucerman
# project: https://github.com/saucer-man/saucer-frame

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
            for payload in payloads:
                vulnurl = url + payload
                try:
                    req = requests.get(vulnurl, headers=headers, timeout=2, verify=False, allow_redirects=False)
                    if req.status_code == 200:
                        with open('result.txt', 'a') as f1:
                            f1.write(vulnurl + '\n')
                        f1.close()
                        print("[+]源码泄露\tpayload: "+vulnurl)
                    # else:
                        # print("[-]不存在源码泄露\tpayload: " + vulnurl)
                except:
                    # print("[-]连接失败\tpayload: "+vulnurl)
                    pass

def usage():
    print('----------------------------')
    print('')
    print("SOURCE LEAK DETECTION")
    print("Usage: ./01.py -u url -l target.txt")
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
                                   ["help=", "url=", "list="])
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

