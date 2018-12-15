#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Xiaobai Lei
from conf import setting
from core import accounts

def make_transaction(account_data, tran_type, amount, log_obj, **kwargs):
    """
    所有交易操作的通用计算
    :param account_data:
    :param tran_type:
    :param amount:
    :param log_obj:
    :param kwargs:
    :return:
    """
    amount = float(amount)  # 将str转换成float
    TRANSACTION_TYPE = setting.TRANSACTION_TYPE     # 读取交易类型
    if tran_type in TRANSACTION_TYPE:
        # 计算利息
        interest = amount * TRANSACTION_TYPE[tran_type]['interest']
        old_credit_balance = account_data['credit_balance']
        # 根据交易类型选择加减
        if TRANSACTION_TYPE[tran_type]['action'] == "plus":
            new_credit_balance = old_credit_balance + amount + interest
            # log_obj.info("操作成功，你的最新余额是%s" % new_credit_balance)
        elif TRANSACTION_TYPE[tran_type]['action'] == "minus":
            new_credit_balance = old_credit_balance - amount - interest
            # 当余额小于0时，交易不成功
            if new_credit_balance < 0:
                print("你的卡余额目前只剩下%s，不足以支付%s" % (old_credit_balance, (amount + interest)))
                # log_obj.error("当前余额不足，操作失败")
                return
            # else:
            #     log_obj.info("操作成功，你的最新余额是%s" % new_credit_balance)
        # 将最新的余额赋值给
        account_data['credit_balance'] = new_credit_balance
        accounts.dump_account(account_data)         # 将修改后的余额写入个人文件，更新数据
        log_obj.info("account:%s   action:%s    amount:%s   interest:%s" %
                     (account_data['id'], tran_type, amount, interest))
        return account_data
    else:
        print("交易类型不存在")

