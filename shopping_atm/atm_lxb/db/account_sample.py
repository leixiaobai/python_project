#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Xiaobai Lei
"""
该脚本主要是为了生成初始化用户，并以json格式保存
"""
import json
import os,sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
from conf import setting
path_msg = setting.DATABASE     # 将setting下DATABASE拿出来
db_path = os.path.join(path_msg["path"], path_msg["name"])  # 将文件存放路径拼凑出来

account_data = {
    "id": 1,
    "username": "xiaobai",
    "password": "123456",
    "credit_limit": 15000,      # 信用卡额度
    "credit_balance": 15000,    # 信用卡余额
    "register_date": "2018-12-01",      # 用户注册时间
    "expire_date": "2028-12-01",        # 用户过期时间，默认十年
    "pay_day":  "22",                    # 还款日期
    "status":   0,                       # 0代表正常，1代表被锁，2代表注销
    "role": "0"                          # 0代表普通用户，x代表管理员
}
db_file = os.path.join(db_path, str(account_data["id"])+".json")
# print(db_file)

with open(db_file, "w") as f:
    f.write(json.dumps(account_data))