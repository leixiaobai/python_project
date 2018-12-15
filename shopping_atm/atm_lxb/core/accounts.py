#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Xiaobai Lei
"""
读取用户个人数据
"""
import json
import os
from core import db_handler
from conf import setting


def load_account(account_id):
    """
    将个人信息从文件中读出
    :param account_id:
    :return:
    """
    db_path = db_handler.db_handler(setting.DATABASE)  # 获取数据文件路径
    account_file = os.path.join(db_path, str(account_id) + ".json")  # 数据文件绝对路径
    if os.path.isfile(account_file):
        with open(account_file, "r") as f:
            account_data = json.load(f)     # 读取文件内的个人数据
        return account_data
    else:
       pass


def dump_account(account_data):
    """
    将个人信息写入文件中（更新）
    :param account_data:
    :return:
    """
    db_path = db_handler.db_handler(setting.DATABASE)  # 获取数据文件路径
    account_file = os.path.join(db_path, str(account_data['id']) + ".json")  # 数据文件绝对路径
    with open(account_file, "w") as f:
        json.dump(account_data, f)     # 将个人数据写入文件
    return True

def is_account(account_id):
    """
    将个人信息从文件中读出
    :param account_id:
    :return:
    """
    db_path = db_handler.db_handler(setting.DATABASE)  # 获取数据文件路径
    account_file = os.path.join(db_path, str(account_id) + ".json")  # 数据文件绝对路径
    if os.path.isfile(account_file):
        return True
    else:
        return False