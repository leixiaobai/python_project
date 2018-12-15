#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Xiaobai Lei
"""
该模块为日志记录模块
"""
import logging
import os
# import sys
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# sys.path.append(BASE_DIR)
from conf import setting

def logger(log_type):
    logger = logging.getLogger(log_type)
    logger.setLevel(setting.LOG_LEVEL)  # 默认日记级别

    log_file = os.path.join(setting.BASE_DIR, "logs", setting.LOG_TYPES[log_type])  # 将日记需要写入的路径导入并拼接
    fh = logging.FileHandler(log_file)  # 创建一个handler，用于写入日志文件
    fh.setLevel(setting.FH_LOG_LEVEL)      # fh日记级别，默认info

    ch = logging.StreamHandler()  # 再创建一个handler，用于输出到控制台
    ch.setLevel(setting.CH_LOG_LEVEL)

    # 创建格式对象，自定义日志输出格式
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    fh.setFormatter(formatter)  # 写入日志文件的格式就用formatter这种
    ch.setFormatter(formatter)  # 输入到控制台格式也用formatter

    logger.addHandler(fh)
    logger.addHandler(ch)

    return logger

if __name__ == '__main__':
    logger = logger("access")
    logger.info("aa")