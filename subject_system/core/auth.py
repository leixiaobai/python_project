#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Xiaobai Lei
import sys
import os
top_path = os.path.dirname(os.path.dirname(__file__))    # 最顶层目录路径
sys.path.append(top_path)   # 加入到系统路径,方便模块导入
from core.handle_db import HandleDb


def login():
    """用户登录认证"""
    count = 3   # 登录尝试3次机会
    while count>0:
        user_msg = HandleDb.read_db() # 默认读取用户信息
        count -= 1
        username = input("请输入用户名:")
        password = input("请输入密码:")
        for msg in user_msg:
            user,passwd,roleid = msg.split("|")    # 获取用户名,密码和权限id
            if user == username and passwd == password:
                print('\033[1;32m登录成功!\033[0m')
                return {"username":username,"roleid":int(roleid)} # 登录成功则返回用户信息和权限id
        else:
            print('\033[1;31m用户名或密码有误!\033[0m')


if __name__ == '__main__':
    # user_msg = handle_db.read_db(username_path)
    # for user in user_msg:
    #     print(user)
    login()