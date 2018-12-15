#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Xiaobai Lei
import os
import sys
import logging

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATABASE = {
    'engine': 'file_storage',   # 文件存储，后续可以支持数据库存储
    'name': 'accounts',         # 数据存放在db下面的目录名称
    'path': BASE_DIR + os.sep + 'db'   # db路径
}

DEFALUT_LOG_LEVEL = logging.INFO      # INFO日记级别
LOG_LEVEL = DEFALUT_LOG_LEVEL       # 设定日志默认级别
FH_LOG_LEVEL = DEFALUT_LOG_LEVEL     # 设定写入文件的日志级别
CH_LOG_LEVEL = DEFALUT_LOG_LEVEL     # 设定写入文件的日志级别

LOG_TYPES = {
    'transaction': 'transactions.log',
    'access': 'access.log',
}

# 交易类型
TRANSACTION_TYPE = {
    'repay':{'action':'plus', 'interest':0},
    'withdraw':{'action':'minus', 'interest':0.05},
    'transfer':{'action':'minus', 'interest':0.05},
    'accept':{'action':'plus', 'interest':0},
    'consume':{'action':'minus', 'interest':0},
}