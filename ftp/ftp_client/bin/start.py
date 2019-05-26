#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Xiaobai Lei
'''整个程序启动入口'''
import sys
import os
top_path = os.path.dirname(os.path.dirname(__file__))    # 最顶层目录路径
sys.path.append(top_path)   # 加入到系统路径,方便模块导入
from core import main

if __name__ == '__main__':
    main.run() #执行程序主函数
