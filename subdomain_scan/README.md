## 子域名扫描脚本

此脚本用来扫描子域名，基于python3，采用多线程暴力破解的方式，字典保存在lib目录下，可指定扫描字典，结果保存在result目录下，可自定结果输出文件名。

### 使用方法

```
usage: subdoman_scan.py [-h] -d DOMAIN [-w WORDLIST] [-t THREADS] [-o OUTFILE]

optional arguments:
  -h, --help            show this help message and exit
  -d DOMAIN, --domain= DOMAIN
                        target domain
  -w WORDLIST, --wordlist= WORDLIST
                        Wordlist
  -t THREADS, --threads= THREADS
                        Number of threads
  -o OUTFILE, --outfile= OUTFILE
                        Write output to file
```
举例：

- 使用帮助
    - python3 subdoman_scan.py -h
    - python3 subdoman_scan.py --help
- 默认扫描
    - python3 subdoman_scan.py --d baidu.com
    - python3 subdoman_scan.py --domain baidu.com
- 高级扫描
    - python3 subdoman_scan.py --d baidu.com -t 30 -w lib/subdomains-100.txt -o result/baidu.txt



## 结果


![](http://ww1.sinaimg.cn/large/005GjT4tgy1fwqmgg9qeaj30or04g3yv.jpg)