#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Xiaobai Lei
'''操作db文件'''


def read_db(file_name):
    '''读取db文件'''
    try:
        f = open(file_name, "r", encoding='utf-8')
        f.readline()    # 把第一行先读取掉
        for line in f:
            yield line
    except Exception as e:
        print(e)
    finally:
        f.close()

def write_db(file_name, file_value):
    '''写入db文件'''
    try:
        f = open(file_name, "a", encoding='utf-8')
        f.write("\n"+file_value)
    except Exception as e:
        print(e)
    finally:
        f.close()