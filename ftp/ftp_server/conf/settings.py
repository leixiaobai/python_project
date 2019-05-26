#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Xiaobai Lei
import os
base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
user_path = os.path.normpath(os.path.join(base_path, 'db', 'userinfo'))
home_path = os.path.normpath(os.path.join(base_path, 'core', 'home'))

md5_salt = "iloveyou"
disk_quotas = 2048     # 默认2G配额
ip_port = ('127.0.0.1', 9999)
status = {'2001':'login',
          '2002':'register'}

user_code = {
    '3001': '用户已存在',
    '3002': '用户注册成功',
    '3003': '用户登录成功',
    '3004': '用户登录失败',}

file_code = {
    '1001': '上传文件,从头开始上传',
    '1002': '上传文件,文件从上一次中断处开始上传',
    '1003': '上传文件成功',
    '1004': '上传文件失败',
    '1005': '下载文件,从头开始下载',
    '1006': '下载文件,文件从上一次中断处开始下载',
    '1007': '下载文件成功',
    '1008': '下载文件失败',
    '1009': '下载文件不存在',
    '1010': '下载文件存在',
    '1011': '文件上传超过配额',
    '1012': '文件上传小于配额',
    '1013': '目录已经存在',
    '1014': '目录不存在',
    '1015': '创建目录成功',
    '1016': '创建目录失败',
}

if __name__ == '__main__':
    print(base_path)
    print(user_path)