#-*- coding:utf-8 -*-

import base64,base58,base91,py3base92,base62
from collections import Counter
import argparse
import os
import sys
import colorama
colorama.init()

parser = argparse.ArgumentParser()
parser.add_argument('-f', type=str, default=None,
                    help='输入加密数据所在文件名称')
parser.add_argument('-t', type=str, default=None,
                    help='直接输入加密数据')
parser.add_argument('--process',action='store_true',
                    help='输出解密过程（密文过长不建议加上次选项）')
args = parser.parse_args()

print('\033[92m******************** 欢迎使用toto的base解密小工具（测试版）********************\033[0m')
print()
flag=args.process
if args.t:
    s=args.t
elif args.f:
    file_path = os.path.join(args.f)
    with open(file_path, "r") as f:
        s="".join(f.readlines()).encode('utf-8')
else:
    print(f'\033[91m-t或者-f参数不能同时为空！\033[0m输入-h查看帮助')
    sys.exit(1)

src=s
cipheylist=[]
while True:
    #base16
    try:
        src=s
        s=base64.b16decode(s)
        str(s,'ascii')
        cipheylist.append('base16')
        if flag:
            print("base16decode:",s)
        continue
    except:
        s=src
        pass
    
    #base32
    try:
        src=s 
        s=base64.b32decode(s)
        str(s,'ascii')
        cipheylist.append('base32')
        if flag:
            print("base32decode:",s)
        continue
    except:
        s=src
        pass

    #base64
    try:
        src=s 
        s=base64.b64decode(s)
        str(s,'ascii')
        cipheylist.append('base64')
        if flag:
            print("base64decode:",s)
        continue
    except:
        s=src
        pass

    #base58
    try:
        src=s 
        s=base58.b58decode(s)
        str(s,'ascii')
        cipheylist.append('base58')
        if flag:
            print("base58decode:",s)
        continue
    except:
        s=src
        pass
    

    #base85(b)
    try:
        src=s
        s=base64.b85decode(s)
        str(s,'ascii')
        cipheylist.append('base85(b)')
        if flag:
            print("base85(b)decode:",s)
        continue
    except:
        s=src
        pass

    #base85(a)
    try:
        src=s 
        s=base64.a85decode(s)
        str(s,'ascii')
        cipheylist.append('base85(a)')
        if flag:
            print("base85(a)decode:",s)
        continue
    except:
        s=src   
        pass
    
    # #base62
    # try:
    #     src=s 
    #     s=base62.decode(s)
    #     str(s,'ascii')
    #     cipheylist.append('base62')
    #     if flag:
    #         print("base62decode:",s)
    #     continue
    # except:
    #     s=src
    #     pass

    # #base91
    # try:
    #     src=s 
    #     s=base91.decode(s)
    #     str(s,'ascii')
    #     cipheylist.append('base91')
    #     if flag:
    #         print("base91decode:",s)
    #     continue
    # except:
    #     s=src
    #     pass



    #base92
    try:
        src=s
        s=str(s,'ascii').replace('\\\\','\\')
        s=py3base92.b92decode(s).encode()
        if not str(s,'ascii').isprintable():
            s=src
            break
        cipheylist.append('base92')
        if flag:
            print("base92decode:",s)
        continue
    except:
        s=src
        pass

    break


def count_characters(lst):
    counts = Counter(lst)
    for key, value in counts.items():
        print(f"{key} 总共执行了 {value} 次，",end='')
    print()

if cipheylist==[]:
    print(f'没有执行任何解密...')
    print()
else:
    print(f"执行的加密/解密过程为: {cipheylist}")
    print()
    count_characters(cipheylist)
    print()

if isinstance(src, str):
    print(f"\033[91m解密失败！\033[0m当前结果为：\033[91m{src}\033[0m")
else:
    print(f"解密成功！结果为：\033[92m{src.decode('utf-8')}\033[0m")   
os.system("pause")