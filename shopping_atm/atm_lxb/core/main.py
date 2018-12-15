#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Xiaobai Lei
import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
from core import logger
from core import auth
from core import creditcard as cc
from core.auth import access_logger
from core import manager_user as mu

# # 用户访问和操作的相关日志
# access_logger = logger.logger("access")
# # 所有的交易日志
# transaction_logger = logger.logger("transaction")

# 用户认证之前初始化信息
user_data ={
    'account_id': None,
    'is_authenticated': False,
    'account_data': None
}


def interactive(user_data):
    """
    用户交互界面，展现atm菜单
    :param user_data:
    :return:
    """
    menu = u'''
       ------ Xiaobai Bank --------
       \033[32;1m 1.  账户信息
       2.  还款
       3.  取款
       4.  转账
       5.  账单
       6.  退出
       \033[0m'''
    menu_dict = {
        "1": cc.account_info,
        "2": cc.repay,
        "3": cc.withdraw,
        "4": cc.transfer,
        "5": cc.pay_check,
        "6": cc.logout,
    }
    exit_flag = True
    while exit_flag:
        print(menu)
        user_choice = input(">>:").strip()
        if user_choice in menu_dict:
            menu_dict[user_choice](user_data)
        else:
            print("你选择的菜单有误，请重新选择")


def main_user():
    """
    用户交互界面，展现用户管理菜单
    :return:
    """
    menu = u'''
       ------ User Manager --------
       \033[32;1m 1.  添加用户
       2.  修改用户
       3.  退出
       \033[0m'''
    menu_dict = {
        "1": mu.add_user,
        "2": mu.change_user,
        "3": mu.logout,
    }
    exit_flag = True
    while exit_flag:
        print(menu)
        user_choice = input(">>:").strip()
        if user_choice in menu_dict:
            menu_dict[user_choice]()
        else:
            print("你选择的菜单有误，请重新选择")


def run():
    """
    主程序启动时运行入口
    :return:
    """
    acc_data = auth.acc_login(user_data, access_logger)     # 用户认证,通过则返回用户个人信息
    if user_data['is_authenticated']:
        user_data['account_data'] = acc_data        # 将个人信息放在account_data下
        print(user_data['account_data'])
        if user_data['account_data']['role'] == "0":
            interactive(user_data)  # atm用户交互
        elif user_data['account_data']['role'] == "x":
            main_user()


if __name__ == '__main__':
    run()