# /usr/bin/env python3
# _*_ coding:utf-8 _*_
# auther: saucerman
# project: https://github.com/saucer-man/penetration-script

"""
decription : 暴力枚举子域名
"""
import sys
import time
import argparse
import threading
import queue
try:
    import dns.resolver
except:
    print("FATAL: Module dnspython missing (try: pip install dnspython)")
    sys.exit(1)

class scanner(threading.Thread):
    def __init__(self,q):
        threading.Thread.__init__(self)
        self.q = q
    def run(self):
        result=[]
        while not self.q.empty():
            domain = self.q.get()
            print(domain+'                   \r', end='', flush=True)
            res = lookup(domain,'A')
            if res:
                for rdata in res:
                    address = rdata.address
                    print('[+]'+domain+' - '+address)
                    result.append(domain+' - '+address)

        print('                                 \r', end ='', flush=True)
        f = open(args.outfile,'a')
        for d in result:
            f.write(d+'\n') 
        f.close()
            
def lookup(domain, recordtype):
    try:
        res = dns.resolver.query(domain, recordtype)
        return res
    except:
        return


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--domain=', help='target domain', dest='domain', required=True)
    parser.add_argument('-w', '--wordlist=', help='Wordlist', dest='wordlist', required=False, default='lib/subdomains-10000.txt')
    parser.add_argument('-t', '--threads=', help='Number of threads', dest='threads', required=False, type=int, default=30)
    parser.add_argument('-o', '--outfile=', help='Write output to file', dest='outfile', required=False)
    args = parser.parse_args()
    return args


if __name__=='__main__':
    global args
    args=get_args()
    # default output filename
    if not args.outfile:
        args.outfile = 'result/'+ args.domain + '.txt'

    q = queue.Queue()
    # Enter the original domain name into the queue
    q.put(args.domain)
    # let domainlist to queue
    with open(args.wordlist, 'r') as f:
        tmps = f.readlines()
        for tmp in tmps:
            url=tmp.strip('\n')+ '.' + args.domain
            q.put(url)

    # Number of threads should be between 1 and 32
    if args.threads < 1:
        args.threads = 1
    elif args.threads > 50:
        args.threads = 50

    print("Start violent cracking\n")
    start = time.time()
    threadslist=[]
    for i in range(args.threads):
        threadslist.append(scanner(q)) 
    for t in threadslist:
        t.start()
        t.join()
    end = time.time()
    print("\nresult has saved in %s" % args.outfile)
    print('Scanner down with %0.6f seconds.'% (end - start))   
