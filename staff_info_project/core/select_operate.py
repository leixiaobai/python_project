#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Xiaobai Lei
import re
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

def sql_deal(sql_field, sql_condtion, read_db_res, staff_lst, sql_sign):
    if sql_sign in sql_condtion:
        con_name, con_value = sql_condtion.split(sql_sign)  # 拿到条件的名字和值
        con_name = con_name.strip()  # 去除多余字符
        con_value = con_value.strip()
        con_name_index = staff_lst.index(con_name)  # 得到条件字段索引
        for line in read_db_res:
            line_lst = line.split(',')  # 通过,分割得到所有的值
            if line_lst:
                sql_if = sign_deal(line_lst[con_name_index], con_value, sql_sign)
                if sql_if:  # 判断条件,如果满足则输出
                    if "," in sql_field:
                        field_lst = []      # 记录字段索引
                        field_name_lst = sql_field.split(',')  # 得到需要输出的字段列表
                        # print(field_name_lst)
                        for field_name in field_name_lst:  # 不知道有多少字段,所有循环取出
                            field_name = field_name.strip()
                            # print(field_name)
                            field_name_index = staff_lst.index(field_name)  # 得到字段索引
                            field_lst.append(field_name_index)          # 将需要打印值的索引添加到列表
                        for field in field_lst:
                            print(line_lst[field].strip('\n'), end=' ')
                        print()
                    elif "*" == sql_field:
                        print(line,end='')  # 直接输出满足条件的所有字段
                    else:
                        field_name_index = staff_lst.index(sql_field)  # 得到字段索引
                        print(line_lst[field_name_index].strip(''))

def select():
    '''用户查询功能
    .可以进行查询，支持三种语法：
    select 列名1，列名2，… where 列名条件
    支持：大于小于等于，还要支持模糊查找。
    '''
    staff_lst = ['id','name','age','phone','job']
    db_file_path = settings.db_file_path
    read_db_res = handle_db.read_db(db_file_path)   # 数据读取结果
    # for i in read_db_res:
    #     print(i.strip())
    select_sql = input("请输入要查询的语句:")    # 用户输入查询语句
    sql_result = re.search('select (.+?) where (.*)', select_sql)    # 通过正则匹配得到要查询的字段和条件
    if sql_result:
        sql_field = sql_result.group(1).strip()    # 需要查询的字段
        sql_condtion = sql_result.group(2).strip()    # 需要查询的条件
        if ">=" in sql_condtion:
            sql_deal(sql_field, sql_condtion, read_db_res, staff_lst, ">=")
        elif ">" in sql_condtion:
            sql_deal(sql_field, sql_condtion, read_db_res, staff_lst, ">")
        elif "<=" in sql_condtion:
            sql_deal(sql_field, sql_condtion, read_db_res, staff_lst, "<=")
        elif "<" in sql_condtion:
            sql_deal(sql_field, sql_condtion, read_db_res, staff_lst, "<")
        elif "=" in sql_condtion:
            sql_deal(sql_field, sql_condtion, read_db_res, staff_lst, "=")
        elif "like" in sql_condtion:
            sql_deal(sql_field, sql_condtion, read_db_res, staff_lst, "like")
        else:
            print("条件有误.")
    else:
        print("请输入合法的sql语句进行查询.")

if __name__ == '__main__':
    select()
