#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Xiaobai Lei

class HandleDb(object):
    """数据库或文件操作相关"""

    def __init__(self):
        pass

    @staticmethod
    def read_file(file_path):
        """读取文件"""
        with open(file_path, "r", encoding="utf8") as f:
            for line in f:
                yield line

    @staticmethod
    def write_file(file_path, file_value):
        """读取文件"""
        with open(file_path, "a", encoding="utf8") as f:
            f.write(file_value+"\n")