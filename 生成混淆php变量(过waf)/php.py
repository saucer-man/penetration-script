import random

def random_keys(len):
    # 生成随机len长的字符串
    str = '`~-=!@#$%^&*_/+?<>{}|:[]abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    return ''.join(random.sample(str,len))

def random_var(len):
    # 生成随机变量名
    str = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    return ''.join(random.sample(str,len))
def xor(c1,c2):
    # 字符亦或，返回16进制
    return hex(ord(c1)^ord(c2)).replace('0x',r"\x")

    
def generate(target):
    key = random_keys(len(target))
    func_line = ''
    call = '$target='
    for i in range(0,len(target)):
        enc = xor(target[i],key[i])
        var = random_var(3)
        func_line += f'$_{var}="{key[i]}"^"{enc}";'
        func_line += '\n'
        call += '$_%s.' % var
    call = call.rstrip('.') + ';'
    print(func_line)
    print(call)
    
if __name__ == '__main__':
    target = input('input target to generate:\r\n') # array_uintersect_uassoc
    generate(target)