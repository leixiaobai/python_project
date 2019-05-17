#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Xiaobai Lei
from core import handle_db
from conf import settings


def create():
    '''用户创建功能'''
    db_file_path = settings.db_file_path
    staff_name = input("请输入新员工姓名:")
    staff_age = input("请输入新员工年龄:")
    staff_phone = input("请输入新员工电话号码:")
    staff_job = input("请输入新员工职位:")
    read_db_res = handle_db.read_db(db_file_path)   # 先读取文件,看目前id序号,返回的是生成器
    for staff_msg in read_db_res:
        staff_info = staff_msg
    staff_info_lst = staff_info.split(',')
    staff_old_index = staff_info_lst[0]     # 获取目前最新的id
    staff_new_index = str(int(staff_old_index) + 1)
    staff_all_value = "%s,%s,%s,%s,%s"%(staff_new_index, staff_name, staff_age, staff_phone, staff_job)
    handle_db.write_db(db_file_path, staff_all_value)

if __name__ == '__main__':
    create()
