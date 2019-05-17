#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Xiaobai Lei
import sys
import os
top_path = os.path.dirname(os.path.dirname(__file__))    # 最顶层目录路径
sys.path.append(top_path)   # 加入到系统路径,方便模块导入
from core import auth
from core.manager import Manager
from core.student import Student
from core.teacher import Teacher

def run():
    """主函数"""
    print('\033[1;42m欢迎您登陆选课系统\033[0m')
    auth_msg = auth.login()    # 接收登录之后的用户信息
    if auth_msg:
        if auth_msg['roleid'] == 0:  # 0表示管理员
            obj = Manager(auth_msg['username'])     # 实例化管理员对象
            while True:
                for i,func in enumerate(Manager.menu, 1):  # 取出类变量进行打印
                    print(i,func[1])
                try:
                    func_num = int(input("请输入功能序号:"))
                    getattr(obj, Manager.menu[func_num-1][0])()     # 根据字符串从对象中找到对应的方法并执行(反射)
                except Exception as e:
                    print("你输入的内容有误")
        elif auth_msg['roleid'] == 1:  # 1表示讲师
            obj = Teacher(auth_msg['username'])  # 实例化管理员对象
            while True:
                for i, func in enumerate(Teacher.menu, 1):  # 取出类变量进行打印
                    print(i, func[1])
                try:
                    func_num = int(input("请输入功能序号:"))
                    getattr(obj, Teacher.menu[func_num - 1][0])()  # 根据字符串从对象中找到对应的方法并执行(反射)
                except Exception as e:
                    print("你输入的内容有误")
        elif auth_msg['roleid'] == 2:  # 2表示学生
            obj = Student(auth_msg['username'])  # 实例化管理员对象
            for i, func in enumerate(Student.menu, 1):  # 取出类变量进行打印
                print(i, func[1])
            try:
                func_num = int(input("请输入功能序号:"))
                getattr(obj, Student.menu[func_num - 1][0])()  # 根据字符串从对象中找到对应的方法并执行(反射)
            except Exception as e:
                print("你输入的内容有误")
        else:
            print("你的角色出了问题,请联系管理员")







if __name__ == '__main__':
    run()