#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Xiaobai Lei
"""
该模块负责所有的数据的交互
"""
import os

def file_db_handle(conn_params):
    """
    返回文件数据存储的路径
    :param conn_params:
    :return:
    """
    db_path = os.path.join(conn_params['path'], conn_params['name'])
    return db_path

def db_handler(conn_params):
    """
    判断连接方式返回不同的连接方法
    :param conn_params:
    :return:
    """
    if conn_params["engine"] == "file_storage":
        return file_db_handle(conn_params)