#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Xiaobai Lei
import time
from core import accounts
from core import logger
# 用户访问和操作的相关日志
access_logger = logger.logger("access")

def login_require(f):
    """
    再次个人信息认证功能
    :param f:
    :return:
    """
    def inner(*args, **kwargs):
        # account_data = accounts.load_account(user_data['account_id'])  # 加载用户最新的数据
        args[0]['is_authenticated'] = False     # 重置用户登录状态，让用户重新登录,args[0]就是
        acc_data = acc_login(args[0], access_logger, 0, args[0]['account_id'])
        if args[0]['is_authenticated']:
            args[0]['account_data'] = acc_data  # 将个人信息放在account_data下
            f(args[0])     # 将认证后的用户传入
    return inner


def acc_auth(account, password):
    """
    用户登录过程的认证
    :param account:
    :param password:
    :return:
    """
    account_data = accounts.load_account(account)   # 从文件中读取个人信息
    if account_data:
        exp_time_stamp = time.mktime(time.strptime(account_data["expire_date"], "%Y-%m-%d"))    # 读取个人过期时间
        if time.time() > exp_time_stamp:
            print("当前用户已过期，请联系管理员")
        elif account_data['status'] == 0:
            if password == account_data['password']:
                return account_data
            else:
                print("用户名或密码错误")
        else:
            if account_data['status'] == 1:
                print("该用户已被锁定")
            elif account_data['status'] == 2:
                print("该用户已被注销")
    else:
        print("该用户不存在")


def lock_auth(account):
    """
    锁定用户
    :param account:
    :return:
    """
    account_data = accounts.load_account(account)
    if account_data:
        if account_data['status'] == 2: # 已经被注销的用户无需锁定
            return None
        else:
            account_data['status'] = 1             # 锁定该用户，1为锁定状态
            # print(account_data)
            accounts.dump_account(account_data)     # 将更新的数据写入文件
            return account_data
    else:
        pass


def acc_login(user_data, log_obj, account_flag = 1, account = None):
    """
    用户登录
    :param user_data:   用户信息
    :param log_obj: 日志
    :param account_flag 是否需要输入账户，1是需要，默认需要
    :param account  用户名
    :return:
    """
    account_dict = {}   # 保存用户输入次数
    retry_flag = True   # 登录重试标志位，单个用户重试超过三次就会变成False
    # retry_count = 0     # 登录重试次数，超过三次就锁定
    while retry_flag and user_data['is_authenticated'] is False:
        if account_flag == 1:
            account = input("Account:").strip()
        password = input("Password:").strip()
        auth = acc_auth(account, password)  # 用户名和密码认证
        if auth:    # 不为空则证明返回了个人信息
            log_obj.info('%s用户登录成功' % auth['username'])
            user_data['is_authenticated'] = True
            user_data['account_id'] = account
            # print(auth)
            return auth
        if account in account_dict:
            account_dict[account] += 1
            if account_dict[account] >= 3:  # 判断同一个用户错误次数是否大于3次
                retry_flag = False
                account_data = lock_auth(account)
                if account_data:
                    log_obj.error("%s用户输入错误超过3次，该用户被锁定" % account_data['username'])
                else:
                    log_obj.error("不存在用户或注销用户累计输入错误超过3次，退出程序")
        else:
            account_dict[account] = 1       # 第一次的用户错误后默认是1