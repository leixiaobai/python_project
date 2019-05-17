#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Xiaobai Lei
import re
import os
from core import handle_db
from conf import settings

def sign_deal(first, second, sign):
    '''通过sign符号返回值'''
    if sign == ">=":
        return first >= second
    elif sign == ">":
        return first > second
    elif sign == "<=":
        return first <= second
    elif sign == "<":
        return first < second
    elif sign == "=":
        return first == second
    elif sign == "like":
        return second in first

def sql_deal(sql_field, sql_condtion, sql_sign):
    if sql_sign in sql_condtion:
        con_name, con_value = sql_condtion.split(sql_sign)  # 拿到条件的名字和值
        con_name = con_name.strip()  # 去除多余字符
        con_value = con_value.strip()
        staff_lst = ['id', 'name', 'age', 'phone', 'job']   # 还可以直接读取文件第一行,这里就直接写了
        con_name_index = staff_lst.index(con_name)  # 得到条件字段索引
        db_file_path = settings.db_file_path
        read_db_res = handle_db.read_db(db_file_path)  # 数据读取结果
        try:
            fw = open(db_file_path+"_副本", "w", encoding='utf-8')    # 打开副本文件
            for line in read_db_res:
                line_lst = line.split(',')  # 通过,分割得到所有的值
                if line_lst:
                    sql_if = sign_deal(line_lst[con_name_index], con_value, sql_sign)
                    if sql_if:  # 判断条件,如果满足则输出
                        field_name,field_value = sql_field.split('=')
                        field_name_index = staff_lst.index(field_name)  # 得到字段索引
                        line_lst[field_name_index] = field_value    # 修改内容
                        staff_info = ','.join(line_lst)             # 新的员工信息
                        fw.write(staff_info)
                    else:
                        fw.write(line)
        except Exception as e:
            print(e)
        finally:
            fw.close()
        os.remove(db_file_path)     # 删除旧的文件
        os.rename(db_file_path+"_副本", db_file_path)

def update():
    '''用户修改功能
    语法：set 列名=“新的值” where 条件
    #先用where查找对应人的信息，再使用set来修改列名对应的值为“新的值”
    set age=27 where id=3
    3,nezha,25,1333235322,IT
    '''
    update_sql = input("请输入修改sql语句:")  # 用户输入修改语句
    sql_result = re.search('set (.+?) where (.*)', update_sql)  # 通过正则匹配得到要修改的字段和条件
    if sql_result:
        sql_field = sql_result.group(1).strip()    # 需要修改的字段
        sql_condtion = sql_result.group(2).strip()    # 需要修改的条件
        if ">=" in sql_condtion:
            sql_deal(sql_field, sql_condtion, ">=")
        elif ">" in sql_condtion:
            sql_deal(sql_field, sql_condtion, ">")
        elif "<=" in sql_condtion:
            sql_deal(sql_field, sql_condtion, "<=")
        elif "<" in sql_condtion:
            sql_deal(sql_field, sql_condtion, "<")
        elif "=" in sql_condtion:
            sql_deal(sql_field, sql_condtion, "=")
        elif "like" in sql_condtion:
            sql_deal(sql_field, sql_condtion, "like")
        else:
            print("条件有误.")
    else:
        print("请输入合法的sql语句进行查询.")

if __name__ == '__main__':
    update()