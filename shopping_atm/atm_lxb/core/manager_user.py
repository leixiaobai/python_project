#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Xiaobai Lei
"""
用户管理模块
"""
import time,datetime
from core import accounts


def account_info(id, username, password = "123", credit_limit = 15000, credit_balance = 15000, status = 0, role = "0",**kwargs):
    now_time = datetime.datetime.now().strftime('%Y-%m-%d')      # 当前时间
    expire_date = (datetime.datetime.now() + datetime.timedelta(days = 3650)).strftime('%Y-%m-%d')   # 十年后过期时间
    account_data = {
        "id": id,
        "username": username,
        "password": password,
        "credit_limit": credit_limit,      # 信用卡额度
        "credit_balance": credit_balance,    # 信用卡余额
        "register_date": now_time,      # 用户注册时间
        "expire_date": expire_date,        # 用户过期时间，默认十年
        "pay_day":  "22",                    # 还款日期
        "status":   status,                       # 0代表正常，1代表被锁，2代表注销
        "role": role                           # 0代表普通用户，x代表管理员
    }
    return account_data


def add_user():
    """
    新建用户
    :return:
    """
    back_flag = True
    while back_flag:
        account_id = input("请输入卡id:")
        if len(account_id) > 0 and account_id.isdigit():
            account_id = int(account_id)
            if not accounts.is_account(account_id):
                username = input("请输入用户名:")
                if len(username) > 0 and username.isalnum():
                    account_data = account_info(account_id, username)   # 返回创建的用户信息
                    accounts.dump_account(account_data)
                    back_flag = False
                else:
                    print("用户名只能是数字和字母")
            else:
                print("卡号已存在")
        elif account_id == "b" or account_id == "back":  # 返回功能
            back_flag = False
        else:
            print("请合法输入卡号或者返回键b")


def change_user():
    back_flag = True
    while back_flag:
        account_id = input("请输入卡id:")
        if len(account_id) > 0 and account_id.isdigit():
            account_data = accounts.load_account(account_id)
            if account_data:
                menu = u'''
                      ------ Change Menu --------
                      \033[32;1m   1.  账户名称
                      2.  账户密码
                      3.  账户额度
                      4.  账户状态
                      5.  账户角色
                      6.  返回
                      \033[0m'''
                menu_dict = {
                    "1": "username",
                    "2": "password",
                    "3": "credit_limit",
                    "4": "status",
                    "5": "role",
                    "6": "b",
                }
                exit_flag = True
                while exit_flag:
                    print(menu)
                    user_choice = input(">>:").strip()
                    if user_choice in menu_dict:
                        if user_choice == "6":  # 退出修改
                            exit_flag = False
                        else:
                            # 目前修改未做任何限制
                            user_info = input("请输入修改后的信息:").strip()
                            account_data[menu_dict[user_choice]] = user_info
                            print(account_data)
                            accounts.dump_account(account_data)         # 写入修改后的数据
                    else:
                        print("你选择的菜单有误，请重新选择")
                # username = input("请输入用户名:")
                # if len(username) > 0 and username.isalpha():
                #     account_data = account_info(account_id, username)  # 返回创建的用户信息
                #     accounts.dump_account(account_data)
                #     back_flag = False
                # else:
                #     print("用户名只能是数字和字母")
            else:
                print("卡号不存在")
        elif account_id == "b" or account_id == "back":  # 返回功能
            back_flag = False
        else:
            print("请合法输入卡号或者返回键b")


def logout():
    """
        实现退出功能
        :return:
        """
    exit()  # 退出程序