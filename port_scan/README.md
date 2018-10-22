## 端口扫描脚本

此脚本是基于nmap开发的端口扫描脚本，包括端口服务扫描和版本探测。

### 优点

- 基于python-nmap模块，相对于一般的socket扫描，隐蔽性更高。
- 扫描速度很快，本来测试了用socket多进程+多线程扫描，但是显然nmap扫描速度快得多。
- 可指定端口或者端口范围，也可以不指定，扫描默认的端口。

### 使用方法举例：
- 单个端口扫描
    - python3 port_scanner.py -h 10.10.10.10 -p 80

- 多个端口扫描
    - python3 port_scanner.py -h 10.10.10.10 -p 80, 81, 443, 8080
    - python3 port_scanner.py -h 10.10.10.10 -p 80-1000
- 扫描默认端口
    - python3 port_scanner.py -h 10.10.10.10 

### 演示截图：

- 单个扫描

![teminal](http://ww1.sinaimg.cn/large/005GjT4tgy1fwh3oaqnb5j30l408vdg6.jpg)

- 批量扫描

![teminal](http://ww1.sinaimg.cn/large/005GjT4tgy1fwh3opukytj30l408vdgj.jpg)

- 默认扫描

![teminal](http://ww1.sinaimg.cn/large/005GjT4tgy1fwh3pt9q10j30l408vmxt.jpg)

