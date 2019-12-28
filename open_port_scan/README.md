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
with open('a.json', 'r', encoding='utf-8') as f:
        f_dict = json.load(f)
        for dic in f_dict:
            for port in dic['ports']:
                port_list.append(port['port'])
port_list = [str(x) for x in sorted(port_list)]
print(",".join(port_list))
```

- nmap 

```
nmap -sS -p1-65535 -oN nmap.txt 10.40.10.191
```

结果为：
```
# Nmap 7.80 scan initiated Sat Dec 28 19:22:19 2019 as: nmap -sS -p1-65535 -oN nmap.txt 10.40.10.191
Nmap scan report for 10.40.10.191
Host is up (0.018s latency).
Not shown: 65515 closed ports
PORT      STATE SERVICE
22/tcp    open  ssh
111/tcp   open  rpcbind
443/tcp   open  https
1947/tcp  open  sentinelsrm
2000/tcp  open  cisco-sccp
2049/tcp  open  nfs
2377/tcp  open  swarm
5060/tcp  open  sip
6379/tcp  open  redis
7778/tcp  open  interwise
7946/tcp  open  unknown
9102/tcp  open  jetdirect
10050/tcp open  zabbix-agent
12004/tcp open  entextlow
13007/tcp open  unknown
27017/tcp open  mongod
35393/tcp open  unknown
35757/tcp open  unknown
35947/tcp open  unknown
51977/tcp open  unknown

# Nmap done at Sat Dec 28 19:40:51 2019 -- 1 IP address (1 host up) scanned in 1112.52 seconds
```

提取出端口：
```
port_list =[]
with open('a.txt', 'r', encoding='utf-8') as f:
        for line in f.readlines():
            if len(line.split("/tcp")) > 1:
                port_list.append(int(line.split("/tcp")[0].strip()))
port_list = [str(x) for x in sorted(port_list)]
print(",".join(port_list))
```