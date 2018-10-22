# /usr/bin/env python3
# _*_ coding:utf-8 _*_
# auther: saucerman
# project: https://github.com/saucer-man/penetration-script

"""
基于python-nmap的端口扫描器
pip install python-nmap
"""

import sys
import nmap
import time 
from colorama import  init, Fore, Back, Style
import getopt

# 颜色定义
init(autoreset=True)
class Colored(object):  
    def red(self, s):
        return Fore.RED + s + Fore.RESET
    def blue(self, s):
        return Fore.BLUE + s + Fore.RESET
    def yellow(self, s):
        return Fore.YELLOW + s + Fore.RESET
color = Colored()

# 使用说明
def usage():
    print(color.blue('Usage: port scanner'))
    print(color.blue('\t-h/--host:\tpoint the target to scan'))
    print(color.blue('\t-p/--port:\tpoint the port to scan(not nessesary)'))
    print(color.blue('Examples:'))
    print(color.blue('\tpython port_scanner.py -h 10.10.10.1'))
    print(color.blue('\tpython port_scanner.py -h 10.10.10.1 -p 80,443,8080'))
    print(color.blue('\tpython port_scanner.py -h 10.10.10.1 -p 1-1024'))
    print(color.blue('\nSEE THE MAN PAGE (https://github.com/saucer-man/saucer-frame) FOR MORE OPTIONS AND EXAMPLES'))
    sys.exit(0)


# 扫描
def scanner(host, ports):
    nm = nmap.PortScanner()
    try:
        print('Scanner report for %s\n'%host)
        if len(ports) == 0:
            result= nm.scan(host)
        else:
            result= nm.scan(host, ports)
        if result['nmap']['scanstats']['uphosts']=='0':
            print(color.red('Host seems down'))
        else:
            print('Host is up')
            print("{:<7}\t{:<7}\t{:<7}\t{:<7}".format('PORT','STATE','SERVICE','VERSION'))
            for k,v in result['scan'][host]['tcp'].items():
                if v['state'] =='open':
                    print(color.yellow("{:<7}\t{:<7}\t{:<7}\t{:<7}".format(str(k),v['state'],v['name'],v['product']+v['version'])))   
                else:
                    print(color.yellow("{:<7}\t{:<7}".format(str(k),v['state'])))
    except Exception as e:
        print(color.red("unhandled Option"))
        usage()
    


def main():
    start =time.time()
    
    # 解析命令行
    if not len(sys.argv[1:]):
        usage()   
    try:
        opts, args = getopt.getopt(sys.argv[1:], "h:p:",
                                   ["host=", "port="])
    except:
        print(color.red("unhandled Option"))
        usage()

    ports=''
    for o, a in opts:
        if o =="-h" or o =="--host":
            host = a
        elif o=="-p" or o == "--port":
            ports = a               

    print("Starting port scanner...")   
    scanner(host,ports)

    end = time.time()
    print('\n\nScanner down with %0.6f seconds.'% (end - start))

if "__main__" == __name__:
    main()