## 信息泄露检测脚本

此脚本用来检测svn、git、DS_Store、hg以及各种备份文件的泄露。字典保存在dictionary.txt，可自行扩展。

例如想扫描是否web目录下存在`beifen.rar`。只要将`\berfen.rar`添加进字典即可。

扫描到的信息泄露结果保存在result.txt中。(没有扫描到漏洞默认不保存）

### 优点

- 基于python3，采用线程池的方法，简单，速度很快。
- 采用状态码和返回包双重检验，几乎不存在误报。
- 扫描字典可自定义，可扩展。

### 使用方法举例：
- 使用帮助
    - python3 source_leak_check.py -h
    - python3 source_leak_check.py --help
- 扫描单个url
    - python3 source_leak_check.py -u www.baidu.com
    - python3 source_leaf_check.py --url=www.baidu.com
- 批量扫描url文本：
    - python3 source_leak_check.py -l target.txt
    - python3 source_leak_check.py -list=target.txt

### 实战举例
可以使用url采集器采集url保存在文本中，然后使用该扫描器。

我用1000条url测试的结果如下：

![teminal](http://ww1.sinaimg.cn/large/005GjT4tgy1fwdlvyv23wj30l409bjrz.jpg)

当出现泄露时，高亮显示：

![teminal](http://ww1.sinaimg.cn/large/005GjT4tgy1fwdlxutn4kj30l409b759.jpg)

最终扫到几十条：

![result](http://ww1.sinaimg.cn/large/005GjT4tgy1fwdm7szfcaj30sh0bgdgj.jpg)

