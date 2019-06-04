import socket
with open('ip.txt', 'w', encoding='utf-8') as f1:
    with open('子域名.txt','r',encoding='utf-8') as f2:
        for d in f2.readlines():
            ip = socket.gethostbyname(d.strip())
            f1.write(str(ip)+'\n')