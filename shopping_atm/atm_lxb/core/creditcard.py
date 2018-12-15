#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Xiaobai Lei
import os
import sys
from core import accounts
from core import transaction
from core import logger
from core import auth
from conf import setting
from core.auth import login_require
# 所有的交易日志
transaction_logger = logger.logger("transaction")


def account_info(user_data):
    """
    列出个人信息
    :param user_data:
    :return:
    """
    user_info = u'''
           ------ %s info --------
           \033[32;1m 
           卡号:  %s
           余额:  %s
           注册时间: %s
           过期时间: %s
           \033[0m''' % (user_data['account_data']['username'], user_data['account_id'],user_data['account_data']['credit_balance'], user_data['account_data']['register_date'], user_data['account_data']['expire_date'])
    print(user_info)


def repay(user_data):
    """
    实现还款功能
    :param user_data:
    :return:
    """
    back_flag = True    # 标志位
    while back_flag:
        account_data = accounts.load_account(user_data['account_id'])  # 加载用户最新的数据
        current_balance = ''' ----- BALANCE INFO -----
            Credit_limit :    %s
            Credit_balance:   %s''' % (account_data['credit_limit'], account_data['credit_balance'])
        print(current_balance)
        repay_amount = input("请输入还款金额：").strip()
        # 用户输入整型数字
        if len(repay_amount) > 0 and repay_amount.isdigit():
            # 如果信用卡余额跟信用卡额度一致则证明没花过钱，则不用还款
            if account_data['credit_balance'] == account_data['credit_limit']:
                print("信用卡已还清，无需还款")
                continue
            elif account_data['credit_balance'] + float(repay_amount) > account_data['credit_limit']:
                print("当前还款金额大于信用卡已使用金额，请输入正确还款金额")
                continue
            new_account_data = transaction.make_transaction(account_data, "repay", repay_amount, transaction_logger)
            if new_account_data:
                print("最新余额为：%s" % new_account_data['credit_balance'])
        elif repay_amount == "b" or repay_amount == "back":         # 返回功能
            back_flag = False
        else:
            print("请合法输入数字或者返回键b")


@login_require
def withdraw(user_data):
    """
    实现取款功能
    :param user_data:
    :return:
    """
    back_flag = True    # 标志位
    while back_flag:
        account_data = accounts.load_account(user_data['account_id'])   # 加载用户最新信息
        current_balance = ''' ----- BALANCE INFO -----
                    Credit_limit :    %s
                    Credit_balance:   %s''' % (account_data['credit_limit'], account_data['credit_balance'])
        print(current_balance)
        withdraw_amount = input("请输入取款金额：").strip()     # 用户输入取款金额
        # 判断用户是否输入整型数字
        if len(withdraw_amount) > 0 and withdraw_amount.isdigit():
            # 取款计算，返回取款后的值
            new_account_data = transaction.make_transaction(account_data, "withdraw", withdraw_amount, transaction_logger)
            if new_account_data:
                print("最新余额为：%s" % new_account_data['credit_balance'])
        elif withdraw_amount == "b" or withdraw_amount == "back":         # 返回功能
            back_flag = False
        else:
            print("请合法输入数字或者返回键b")


@login_require
def transfer(user_data):
    """
    实现转账功能
    :param user_data:
    :return:
    """
    back_flag = True  # 标志位
    while back_flag:
        account_data = accounts.load_account(user_data['account_id'])  # 加载用户最新信息
        current_balance = ''' ----- BALANCE INFO -----
                        Credit_limit :    %s
                        Credit_balance:   %s''' % (account_data['credit_limit'], account_data['credit_balance'])
        print(current_balance)
        transfer_account = input("请输入收款人账号：").strip()  # 用户输入收款人账号
        if transfer_account.isdigit():
            transfer_account_data = accounts.load_account(int(transfer_account))  # 加载收款人用户信息
            if not transfer_account_data:                   # 判断是否存在该卡号
                print("你输入的卡号有误，请重新输入")
                continue
            transfer_amount = input("请输入转账金额：").strip()  # 用户输入转账金额
            # 判断用户是否输入整型数字
            if len(transfer_amount) > 0 and transfer_amount.isdigit():
                # 当前卡转账后剩余的钱
                new_account_data = transaction.make_transaction(account_data, "withdraw", transfer_amount, transaction_logger)
                if new_account_data:
                    # 收款方进账的钱
                    new_transfer_account_data = transaction.make_transaction(transfer_account_data, "accept", transfer_amount, transaction_logger)
                    print("当前卡最新余额为：%s" % new_account_data['credit_balance'])
            elif transfer_amount == "b" or transfer_amount == "back":  # 返回功能
                back_flag = False
            else:
                print("请合法输入数字或者返回键b")
        elif transfer_account == "b" or transfer_account == "back":         # 返回功能
            back_flag = False
        else:
            print("请合法输入数字或者返回键b")


def pay_check(user_data):
    """
    查看账单
    :param user_data:
    :return:
    """
    # log_time = input("请输入开始时间，格式为Y-M-D").strip()
    transaction_log = os.path.join(setting.BASE_DIR, "logs", setting.LOG_TYPES['transaction'])
    with open(transaction_log, "r") as log_f:
        for i in log_f:
            if "account:%s"%(user_data['account_id']) in i:
                print(i, end='')


def logout(user_data):
    """
    实现退出功能
    :return:
    """
    account_info(user_data)         # 打印个人账户信息
    exit()                          # 退出程序

if __name__ == '__main__':
    repay(user_data)