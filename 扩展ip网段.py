import ipaddress

net4 = ipaddress.ip_network('120.78.0.0/16', strict=False)
with open('b.txt','w',encoding='utf-8') as f:
    for x in net4.hosts():
        f.write(str(x)+'\n')