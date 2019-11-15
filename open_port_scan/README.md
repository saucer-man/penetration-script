- shell命令
```
# 全部开放的端口
echo $(netstat -antlp|awk -F ':' '{print $2}'| awk '{print $1}'|grep -v "^$"|sort -n| uniq) | sed 's/[ ][ ]*/,/g'

# listen中的端口
echo $(netstat -ntlp|awk -F ':' '{print $2}'| awk '{print $1}'|grep -v "^$"|sort -n| uniq) | sed 's/[ ][ ]*/,/g'
```

- masscan
```
masscan -p1-65535 -oJ a.json 192.168.1.0
```
结果为
```
[
{   "ip": "10.40.57.81",   "timestamp": "1572233567", "ports": [ {"port": 2049, "proto": "tcp", "status": "open", "reason": "syn-ack", "ttl": 128} ] },
{   "ip": "10.40.57.81",   "timestamp": "1572233571", "ports": [ {"port": 10259, "proto": "tcp", "status": "open", "reason": "syn-ack", "ttl": 128} ] },
]
```
去除最后的，然后用用python提取出来
```
import json
port_list =[]
with open('C:\\Users\\ttt\\Desktop\\a.json', 'r', encoding='utf-8') as f:
        f_dict = json.load(f)
        for dic in f_dict:
            for port in dic['ports']:
                port_list.append(port['port'])
print(port_list)
```