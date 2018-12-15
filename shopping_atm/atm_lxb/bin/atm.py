#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Xiaobai Lei
import os
import sys
# 添加环境变量
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
from core import main

if __name__ == '__main__':
    # 执行主程序
    main.run()