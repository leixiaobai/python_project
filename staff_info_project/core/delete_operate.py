#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Xiaobai Lei
import os
from core import handle_db
from conf import settings

def delete():
    '''用户删除功能
    '''
    db_file_path = settings.db_file_path
    # read_db_res = handle_db.read_db(db_file_path)  # 先读取文件,看目前序号最大多少
    try:  # 捕捉用户输入的异常
        delete_staff_num = input("请选择需要删除的员工id:").strip()
        f1 = open(db_file_path, "r", encoding='utf-8')
        f2 = open(db_file_path+"_副本", "w", encoding='utf-8')
        for line in f1:
            line_lst = line.split(',')
            if delete_staff_num == line_lst[0]:
                continue
            else:
                f2.write(line)
    except ValueError as e:
        print("你输入的有误,请输入数字!")
    except Exception as e:
        print(e)
    finally:
        f1.close()
        f2.close()
    os.remove(db_file_path)
    os.rename(db_file_path + "_副本", db_file_path)

if __name__ == '__main__':
    delete()